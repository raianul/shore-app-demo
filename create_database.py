import sqlalchemy

from shore_app.models import User

from shore_app.app import create_app
from shore_app.extensions import db
from shore_app.config import DefaultConfig


def run():
    config = DefaultConfig
    db.create_all(app=create_app(config))


if __name__ == '__main__':
    print("Creating tables")
    run()
    print("Done")
