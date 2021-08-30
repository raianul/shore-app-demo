import os


STRING_LEN = 225


class BaseConfig(object):

    PROJECT = "shore_app"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['raianul.kabir@gmail.com']
    LOG_FOLDER = os.path.join(os.path.join('/var/log', 'shore_app'))


class DefaultConfig(BaseConfig):

    DEBUG = True

    DB_NAME = 'shoreapp'

    # EMAIL SETTINGS
    SENT_EMAIL = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'pranto157@gmail.com'
    MAIL_PASSWORD = 'Pr@nto261984'

    # MYSQL
    SQLALCHEMY_DATABASE_URI = 'mysql://shore:qwe90qwe@shore-app-db/%s?charset=utf8' % DB_NAME

    # Redis
    SUB_SCHEDULE_TIME = 60  # in seconds
    PROD_SCHEDULE_TIME = 60  # in seconds
    CELERY_BROKER_URL = 'redis://redis:6379'
    CELERY_RESULT_BACKEND = 'redis://redis:6379'

    # EBAY Host
    EBAY_HOST = 'https://api.sandbox.ebay.com/shopping'

    # EBAY API Params
    EBAY_API_PARAMS = {
        'MaxEntries': 20,
        'AvailableItemsOnly': True,
        'responseencoding': 'JSON',
        'appid': 'SayedKab-shoreapp-SBX-21d98cfe6-67df03b3',
        'version': '1157'
    }


class TestConfig(BaseConfig):
    DB_NAME = 'shoreapp_test'
    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

    # MYSQL
    SQLALCHEMY_DATABASE_URI = 'mysql://shore:qwe90qwe@shore-app-db/%s?charset=utf8' % DB_NAME
