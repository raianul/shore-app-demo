from flask_testing import TestCase

from shore_app import create_app
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
