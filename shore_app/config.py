import os

from shore_app.utils import make_dir, INSTANCE_FOLDER_PATH


class BaseConfig(object):

    PROJECT = "shore_app"

    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['raianul.kabir@gmail.com']

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH)


class DefaultConfig(BaseConfig):

    DEBUG = True

    MAIL_HOST = ""
    FROM_ADDR = ""
    TO_ADDRS = [""]
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""

    # MYSQL
    SQLALCHEMY_DATABASE_URI = 'mysql://shore:qwe90qwe@shore-app-db/shoreapp?charset=utf8'


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

    # MYSQL
    SQLALCHEMY_DATABASE_URI = 'mysql://shore:qwe90qwe@shore-app-db/shoreapp_test?charset=utf8'
