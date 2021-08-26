import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify

from shore_app.config import DefaultConfig
from shore_app.extensions import db

# For import *
__all__ = ['create_app']


def create_app(config=None, app_name=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = config.PROJECT

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app, config)
    configure_extensions(app)
    configure_logging(app)
    return app


def configure_app(app, config=None):
    app.config.from_object(config)


def configure_extensions(app):
    db.init_app(app)


def configure_logging(app):
    app.logger.setLevel(logging.INFO)
    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = RotatingFileHandler(
        info_log, mode='w', maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # # Testing
    # app.logger.info("testing info.")
    # app.logger.warn("testing warn.")
    # app.logger.error("testing error.")


app = create_app(DefaultConfig)


@app.route('/status')
def status():
    db.session.execute('select 1').scalar()
    data = {'status': 'OK'}
    return jsonify(data), 200


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
