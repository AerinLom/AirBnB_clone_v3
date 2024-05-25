#!/usr/bin/python3
"""
Routes for handling user objects through the api
"""
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """
    collects list of all places
    """
    all_places = [
        place.to_dict()
        for place in storage.all(Place).values()
    ]
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    collects place object by id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes place object by id
    """
    place_to_delete = storage.get(Place, place_id)
    if not place_to_delete:
        return abort(404)
    storage.delete(place_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    creates place object
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if data is None:
        return abort(400, 'Not a JSON')
    if 'user_id' not in data:
        return abort(400, 'Missing user_id')
    if 'name' not in data:
        return abort(400, 'Missing name')

    user = storage.get('User', data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id

    place_to_create = Place(**data)
    storage.new(place_to_create)
    storage.save()
    return jsonify(place_to_create.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    update place object
    """
    place_to_update = storage.get(Place, place_id)
    if place_to_update:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place_to_update, key, value)
        storage.save()
        return jsonify(place_to_update.to_dict()), 200
    else:
        return abort(404)
