#!/usr/bin/python3
"""
Routes for handling user objects through the api
"""
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Gets all place objects
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    all_places = storage.all('Place')
    city_places = [place_obj.to_dict() for place_obj in all_places.values()
                   if obj.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Returns a place object
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place object
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a place object
    """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)

    data = request.get_json()
    if not data:
        return abort(400, 'Not a JSON')
    if 'user_id' not in data:
        return abort(400, 'Missing user_id')
    if 'name' not in data:
        return abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place object
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    data = request.get_json()
    if not data:
        return abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
