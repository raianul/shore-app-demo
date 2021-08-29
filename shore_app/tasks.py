from datetime import datetime, timedelta
import os
import time

# from celery import Celery

from shore_app.extensions import celery, db, mail
from shore_app.config import DefaultConfig
from shore_app.models import Subscription
from shore_app.utils import send_mail, get_current_time, commit_or_rollback
from shore_app.app import app
from shore_app.extensions import db
from shore_app.api.ebay import Ebay


# celery = Celery(__name__)
celery.conf.broker_url = DefaultConfig.CELERY_BROKER_URL
celery.conf.result_backend = DefaultConfig.CELERY_RESULT_BACKEND


CELERYBEAT_SCHEDULE = {
    'run-every-sixty-seconds': {
        'task': 'shore_app.tasks.create_task',
        'schedule': 60
    },
}

celery.conf.beat_schedule = CELERYBEAT_SCHEDULE


@celery.task
def create_task():
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


def _sent_email_notification(sub):
    response = _get_ebay_response(sub.phrases)

    if not response:
        return

    subject = "Your %s minutes update from Ebay" % sub.interval
    try:
        if os.environ['FLASK_MAIL'] != 'disabled':
            send_mail(mail, subject, sub.user, response)
        app.logger.info("Successfully sent email to - %s" % sub.user.email)
    except Exception:
        app.logger.error("Mail sent failed to - %s" % sub.user.email)
        return

    return True

    # celery -A shore_app.tasks.celery worker --loglevel=info
    # celery -A shore_app.tasks.celery beat --loglevel=info

    # https://api.sandbox.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=SayedKab-shoreapp-SBX-21d98cfe6-67df03b3&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=harry%20potter%20phoenix&paginationInput.entriesPerPage=2
