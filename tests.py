import unittest
import json
import sqlalchemy
from flask_testing import TestCase

from shore_app import create_app
from shore_app.models import User
from shore_app.config import TestConfig
from shore_app.extensions import db


class BaseTestCase(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def init_data(self):
        raise NotImplementedError

    def setUp(self):
        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.session.remove()
        db.drop_all()

    def _test_get_request(self, endpoint):
        response = self.client.get(endpoint)
        self.assert_200(response)
        return response


class TestUserResource(BaseTestCase):

    post_data = {
        'name': 'Sayed Raianul Kabir',
        'email': 'raianul.kabir@gmail.com',
        'subscribe': True
    }

    def init_data(self):
        demo1 = User(
            name=u'demo1',
            email=u'demo1@example.com',
            subscribe=True)
        demo2 = User(
            name=u'demo2',
            email=u'demo2@example.com',
            subscribe=True)
        db.session.add(demo1)
        db.session.add(demo2)
        db.session.commit()

    def test_list_users(self):
        response = self._test_get_request('/api/users')
        assert len(response.json) == 2

    def test_get_user(self):
        response = self._test_get_request('/api/user/1')
        assert response.json['email'] == 'demo1@example.com'

    def test_post_user(self):
        response = self.client.post(
            '/api/users', data=json.dumps(self.post_data), content_type='application/json')
        assert response.status == '200 OK'
        new_user = User.query.filter_by(email=self.post_data['email']).first()
        assert new_user.name == "Sayed Raianul Kabir"

    def test_delete_user(self):
        response = self.client.delete('/api/user/1')
        assert response.status == '200 OK'
        assert not User.query.filter_by(email='demo1@example.com').first()

    def test_put_user(self):
        response = self.client.put(
            '/api/user/1', data=json.dumps({'email': 'raian@gmail.com'}), content_type='application/json')
        assert response.status == '200 OK'
        user = User.query.filter_by(email='raian@gmail.com').first()
        assert user.name == "demo1"


if __name__ == '__main__':
    unittest.main()
