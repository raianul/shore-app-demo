import json
from unittest import mock
from datetime import datetime, timedelta

from .base import BaseTestCase
from shore_app.extensions import db
from shore_app.models import Subscription, User


class TestEmailAlert(BaseTestCase):

    def init_data(self):

        # create a user
        user = User(
            name=u'user',
            email=u'user@example.com')

        db.session.add(user)

        # create multiple subscriptions with different interval
        sub1 = Subscription(phrases='p1', interval=2, user=user)
        sub2 = Subscription(phrases='p2', interval=10, user=user)
        sub3 = Subscription(phrases='p3', interval=30, user=user)

        db.session.add(sub1)
        db.session.add(sub2)
        db.session.add(sub3)
        # Commit Data
        db.session.commit()

    @mock.patch('shore_app.models.subscription.datetime')
    def test_sent_alert_if_all_interval_match(self, mock_dt):
        mock_dt.utcnow.return_value = datetime(
            datetime.utcnow().year + 1, 1, 1)

        for sub in Subscription.query.all():
            assert sub.valid_for_alert == True

    @mock.patch('shore_app.models.subscription.datetime')
    def test_sent_alert_if_all_interval_not_match(self, mock_dt):
        mock_dt.utcnow.return_value = datetime.utcnow() + timedelta(minutes=1)

        for sub in Subscription.query.all():
            assert sub.valid_for_alert == False

    @mock.patch('shore_app.models.subscription.datetime')
    def test_sent_alert_if_interval_match_only_with_two_min(self, mock_dt):
        sub = Subscription.query.filter_by(interval=2).one()

        # increasing 3 min with the last email sent
        mock_dt.utcnow.return_value = sub.last_email_sent + \
            timedelta(minutes=3)

        for sub in Subscription.query.all():
            if sub.interval == 2:
                assert sub.valid_for_alert == True
            else:
                assert sub.valid_for_alert == False

    @mock.patch('shore_app.models.subscription.datetime')
    def test_sent_alert_if_interval_match_only_with_ten_min(self, mock_dt):
        sub_2 = Subscription.query.filter_by(interval=2).one()
        # Changing the interval last_email, assuming it was already sent
        sub_2.last_email_sent = sub_2.last_email_sent + \
            timedelta(minutes=9)
        db.session.add(sub_2)
        db.session.commit()

        sub_10 = Subscription.query.filter_by(interval=10).one()
        # increasing 10 min with the last email sent
        mock_dt.utcnow.return_value = sub_10.last_email_sent + \
            timedelta(minutes=10)

        for sub in Subscription.query.all():
            if sub.interval == 10:
                assert sub.valid_for_alert == True
            else:
                assert sub.valid_for_alert == False

    @mock.patch('shore_app.models.subscription.datetime')
    def test_sent_alert_if_interval_match_only_with_thirty_min(self, mock_dt):
        sub_2 = Subscription.query.filter_by(interval=2).one()
        # Changing the interval last_email, assuming it was already sent
        sub_2.last_email_sent = sub_2.last_email_sent + \
            timedelta(minutes=29)
        db.session.add(sub_2)

        sub_10 = Subscription.query.filter_by(interval=10).one()
        sub_10.last_email_sent = sub_10.last_email_sent + \
            timedelta(minutes=25)
        db.session.add(sub_10)

        db.session.commit()
        # increasing 30 min with the last email sent
        sub_30 = Subscription.query.filter_by(interval=30).one()
        mock_dt.utcnow.return_value = sub_30.last_email_sent + \
            timedelta(minutes=30)
        for sub in Subscription.query.all():
            if sub.interval == 30:
                assert sub.valid_for_alert == True
            else:
                assert sub.valid_for_alert == False

    @mock.patch('shore_app.models.subscription.datetime')
    def test_sent_alert_if_interval_match_only_with_ten_and_thirty_min(self, mock_dt):
        sub_2 = Subscription.query.filter_by(interval=2).one()
        # Changing the interval last_email, assuming it was already sent
        sub_2.last_email_sent = sub_2.last_email_sent + \
            timedelta(minutes=34)
        db.session.add(sub_2)

        sub_10 = Subscription.query.filter_by(interval=10).one()
        sub_10.last_email_sent = sub_10.last_email_sent + \
            timedelta(minutes=25)
        db.session.add(sub_10)

        db.session.commit()
        # increasing 30 min with the last email sent
        sub_30 = Subscription.query.filter_by(interval=30).one()
        mock_dt.utcnow.return_value = sub_30.last_email_sent + \
            timedelta(minutes=35)
        for sub in Subscription.query.all():
            if sub.interval in [10, 30]:
                assert sub.valid_for_alert == True
            else:
                assert sub.valid_for_alert == False
