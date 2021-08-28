import json
from flask import Blueprint, request, jsonify, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from shore_app.extensions import db
from shore_app.models import User
from shore_app.utils import commit_or_rollback


class UserItem(Resource):

    def _get_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, "User not found for id -  %s" % user_id)
        return user

    def get(self, user_id):
        user = self._get_user(user_id)
        user = user.serialize()
        del user['subscribtions']
        return jsonify(user)

    def delete(self, user_id):
        user = self._get_user(user_id)
        db.session.delete(user)
        commit_or_rollback(db.session)
        jsonify({'message': 'User id %s succsesfully removed' % user_id})

    def put(self, user_id):
        user_json = request.get_json(force=True)
        user = User.query.get(user_id)
        user = _set_attributes(user, user_json)
        try:
            db.session.add(user)
            commit_or_rollback(db.session)
        except IntegrityError as e:
            abort(400, e.orig.args[1])

        user = user.serialize()
        del user['subscribtions']
        return jsonify(user)


class UserItems(Resource):

    def get(self):
        users = User.query.all()
        users = [{x: d[x] for x in d if x != 'subscribtions'}
                 for d in User.serialize_list(users)]
        return jsonify(users)

    def post(self):
        user_json = request.get_json(force=True)
        user = User()
        user = _set_attributes(user, user_json)
        try:
            db.session.add(user)
            commit_or_rollback(db.session)
        except IntegrityError as e:
            abort(400, e.orig.args[1])
        return jsonify(user.serialize())


def _set_attributes(user, user_json):
    for attr in ['name', 'email', 'subscribe_alert', 'active']:
        if user_json.get(attr):
            try:
                setattr(user, attr, user_json[attr])
            except ValueError as e:
                abort(400, str(e))
    return user
