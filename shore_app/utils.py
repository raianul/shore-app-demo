import string
import random
import os
import json
import datetime

from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.inspection import inspect


# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/var/log', 'shore_app')

# Model
STRING_LEN = 64


def get_current_time():
    return datetime.datetime.utcnow()


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e


def commit_or_rollback(session):
    try:
        session.commit()
    except (DBAPIError, IntegrityError):
        session.rollback()
        raise


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # return int(obj.strftime('%s'))
            return str(obj)
        elif isinstance(obj, datetime.date):
            # return int(obj.strftime('%s'))
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
