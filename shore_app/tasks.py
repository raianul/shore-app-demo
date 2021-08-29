from datetime import datetime, timedelta
import os
import time
from sqlalchemy.exc import IntegrityError

from shore_app.extensions import celery, db, mail
from shore_app.config import DefaultConfig
from shore_app.models import Subscription, Product, User
from shore_app.utils import send_mail, get_current_time, commit_or_rollback
from shore_app.app import app
from shore_app.extensions import db
from shore_app.api.ebay import Ebay


celery.conf.broker_url = DefaultConfig.CELERY_BROKER_URL
celery.conf.result_backend = DefaultConfig.CELERY_RESULT_BACKEND


CELERYBEAT_SCHEDULE = {
    'check_subscription': {
        'task': 'shore_app.tasks.check_subscription',
        'schedule': app.config.get('SUB_SCHEDULE_TIME')
    },
    'create_product': {
        'task': 'shore_app.tasks.create_product',
        'schedule': app.config.get('PROD_SCHEDULE_TIME'),
        'args': (['sub'], ['response'])
    },
}

celery.conf.beat_schedule = CELERYBEAT_SCHEDULE


@celery.task(bind=True,  queue='check_subscription')
def check_subscription(self):
    for sub in Subscription.query.all():
        if sub.sent_email and _sent_email_notification(sub):
            app.logger.info("Processing alert email for  - %s" %
                            sub.user.email)
            sub.last_email_sent = get_current_time()
            app.logger.info(
                "Successfully updated last email sent time for  - %s" % sub.user.email)

    commit_or_rollback(db.session)


def _get_ebay_response(query):
    response = Ebay('findItemsAdvanced').search(query=query)
    if response.get('Ack') == 'Failure':
        app.logger.error(response)
        return

    if 'SearchResult' not in response:
        app.logger.info("No result found for query - %s" % query)
        return

    response['SearchResult'] = response['SearchResult'][0]['ItemArray']['Item']

    return response


@celery.task
def create_product(sub, response):
    user = User.query.get(sub['user_id'])
    products = []
    app.logger.info("Creating Product from search result")
    for resp in response['SearchResult']:
        product, created = Product.get_or_create(phrases=sub['phrases'], item_id=resp['ItemID'], defaults={
            'title': resp['Title'],
            'end_time': datetime.strptime(resp['EndTime'], "%Y-%m-%dT%H:%M:%S.%f%z"),
            'price': resp['ConvertedCurrentPrice']['Value'],
            'currency': resp['ConvertedCurrentPrice']['CurrencyID']
        })

        if not created:
            product.last_price = product.price
            product.price = resp['ConvertedCurrentPrice']['Value']
            commit_or_rollback(db.session)

        if product not in user.products:
            products.append(product)
    user.products.extend(products)
    try:
        commit_or_rollback(db.session)
    except IntegrityError as e:
        app.logger.error(e)


def _sent_email_notification(sub):
    response = _get_ebay_response(sub.phrases)
    if not response:
        return

    create_product.apply_async(
        args=[sub.serialize(), response], queue='create_product')

    subject = "Your %s minutes update from Ebay" % sub.interval
    try:
        if os.environ['FLASK_MAIL'] != 'disabled':
            send_mail(mail, subject, sub.user, response)
        app.logger.info("Successfully sent email to - %s" % sub.user.email)
    except Exception:
        app.logger.error("Mail sent failed to - %s" % sub.user.email)
        return

    return True
