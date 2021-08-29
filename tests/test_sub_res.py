import json

from .base import BaseTestCase
from shore_app.extensions import db
from shore_app.models import Subscription, User


class TestSubscribeResource(BaseTestCase):

    post_data = {
        'phrases': 'Test Phrase',
        'interval': 10,
    }

    def init_data(self):

        user_data = User(
            name=u'demo3',
            email=u'demo3@example.com',
            subscribe=True)
        db.session.add(user_data)
        sub_data = Subscription(phrases='test', interval=2)
        user_data.subscribtions.append(sub_data)

        db.session.add(sub_data)
        db.session.commit()

    def test_list_subs(self):
        response = self._test_get_request('/api/subscriptions')
        assert len(response.json) == 1

    def test_get_sub(self):
        response = self._test_get_request('/api/subscription/1')
        assert response.json['phrases'] == 'test'

    def test_post_sub(self):
        user = User.query.filter_by(email='demo3@example.com').first()
        self.post_data['user_id'] = user.id
        response = self.client.post(
            '/api/subscriptions', data=json.dumps(self.post_data), content_type='application/json')
        assert response.status == '200 OK'
        sub = Subscription.query.filter_by(
            phrases=self.post_data['phrases']).first()
        assert sub.phrases == "Test Phrase"

    def test_put_sub(self):
        response = self.client.put(
            '/api/subscription/1', data=json.dumps({'interval': 45}), content_type='application/json')
        assert response.status == '200 OK'

    def test_delete_sub(self):
        response = self.client.delete('/api/subscription/1')
        assert response.status == '200 OK'
