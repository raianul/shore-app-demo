import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from shore_app.app import app
from shore_app.extensions import celery, db, mail
from shore_app.config import DefaultConfig
from shore_app.models import Subscription, Product
from shore_app.utils import send_mail, get_current_time, commit_or_rollback
from shore_app.api.ebay import Ebay


celery.conf.broker_url = DefaultConfig.CELERY_BROKER_URL
celery.conf.result_backend = DefaultConfig.CELERY_RESULT_BACKEND


CELERYBEAT_SCHEDULE = {
    'create_product_from_ebay': {
        'task': 'shore_app.tasks.create_product_from_ebay',
        'schedule': app.config.get('SUB_SCHEDULE_TIME')
    },
    'check_subscription_and_sent_alert': {
        'task': 'shore_app.tasks.check_subscription_and_sent_alert',
        'schedule': app.config.get('PROD_SCHEDULE_TIME'),
    },
}

celery.conf.beat_schedule = CELERYBEAT_SCHEDULE


@celery.task(bind=True,  queue='create_product_from_ebay')
def create_product_from_ebay(self):
    for sub in Subscription.query.all():
        ebay_resp = _get_ebay_response(sub.phrases)
        if not ebay_resp:
            continue
        create_product(sub, ebay_resp)


@celery.task(bind=True,  queue='check_subscription_and_sent_alert')
def check_subscription_and_sent_alert(self):
    for sub in Subscription.query.all():
        if sub.valid_for_alert and _sent_email_notification(sub):
            app.logger.info("Processing alert email for  - %s" %
                            sub.user.email)
            sub.last_email_sent = get_current_time()
            app.logger.info(
                "Successfully updated last email sent time for  - %s" % sub.user.email)

    commit_or_rollback(db.session)


def _get_ebay_response(query):
    app.logger.info("Fetching results from ebay....")
    response = Ebay('findItemsAdvanced').search(query=query)
    if response.get('Ack') == 'Failure':
        app.logger.error(response)
        return

    if 'SearchResult' not in response:
        app.logger.info("No result found for query - %s" % query)
        return

    response['SearchResult'] = response['SearchResult'][0]['ItemArray']['Item']

    return response


def create_product(sub, response):
    products = []

    for resp in response['SearchResult']:
        product, created = Product.get_or_create(item_id=resp['ItemID'], defaults={
            'title': resp['Title'],
            'link': resp['ViewItemURLForNaturalSearch'],
            'end_time': datetime.strptime(resp['EndTime'], "%Y-%m-%dT%H:%M:%S.%f%z"),
            'price': resp['ConvertedCurrentPrice']['Value'],
            'currency': resp['ConvertedCurrentPrice']['CurrencyID']
        })

        product.last_price = product.price
        if not created:
            product.price = resp['ConvertedCurrentPrice']['Value']
            commit_or_rollback(db.session)

        if product not in sub.products:
            products.append(product)
    sub.products.extend(products)
    try:
        app.logger.info("Creating/Updating Product from search result")
        commit_or_rollback(db.session)
    except IntegrityError as e:
        app.logger.error(e)


def _sent_email_notification(sub):

    product_insights = Product.product_insights(sub.products)

    if not product_insights:
        return False

    if app.config.get('SENT_EMAIL', False):
        try:
            subject = "Your %s minutes update from Ebay for %s" % (
                sub.interval, sub.phrases)
            send_mail(mail, subject, sub.user, sub.phrases, product_insights)
            app.logger.info("Successfully sent email to - %s" % sub.user.email)
        except Exception:
            app.logger.error("Mail sent failed to - %s" % sub.user.email)
            return
    else:
        app.logger.info(
            "DRY MODE: Successfully sent email to - %s" % sub.user.email)

    return True
