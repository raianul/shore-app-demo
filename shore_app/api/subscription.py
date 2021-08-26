import json
from flask import Blueprint, request, jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from shore_app.extensions import db
from shore_app.models import Subscription
from shore_app.utils import commit_or_rollback


class SubscriptionItem(Resource):

    def _get_subscription(self, sub_id):
        user = Subscription.query.get(sub_id)
        if not user:
            abort(404, "Subscription not found for id -  %s" % sub_id)
        return user

    def get(self, sub_id):
        user = self._get_subscription(sub_id)
        return jsonify(user.serialize())

    def delete(self, sub_id):
        user = self._get_subscription(sub_id)
        db.session.delete(user)
        commit_or_rollback(db.session)
        jsonify({'message': 'Subscription id %s succsesfully removed' % sub_id})

    def put(self, sub_id):
        user_json = request.get_json(force=True)
        user = Subscription.query.get(sub_id)
        user = _set_attributes(user, user_json)
        try:
            db.session.add(user)
            commit_or_rollback(db.session)
        except IntegrityError as e:
            abort(400, e.orig.args[1])
        return jsonify(user.serialize())


class SubscriptionItems(Resource):

    def get(self):
        subs = Subscription.query.all()
        return jsonify(Subscription.serialize_list(subs))

    def post(self):
        sub_json = request.get_json(force=True)
        sub = Subscription()
        sub = _set_attributes(sub, sub_json)
        try:
            db.session.add(sub)
            commit_or_rollback(db.session)
        except IntegrityError as e:
            abort(400, e.orig.args[1])
        return jsonify(sub.serialize())


def _set_attributes(user, sub_json):
    for attr in ['user_id', 'phrases', 'interval', 'active']:
        if sub_json.get(attr):
            try:
                setattr(user, attr, sub_json[attr])
            except ValueError as e:
                abort(400, str(e))
    return user
