#!/usr/bin/python3
"""
create new users
"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """
    collects list of all users
    """
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """
    collects user object
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)

@app_views.route('/users/<user_id>',methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    collects user object
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
    else:
        return abort(404)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    creates user object
    """
    if request.content_type != 'application\json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        return abort(400, 'Missing name')
    if 'password' not in data:
        return abort(400, 'Missing password')

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    update user object
    """
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            return abort(404, 'Not a JSON')
        if request.content_type != 'application/json':
            return abort(404, 'Not a JSON')
        data = request.get_json()

        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(404)
