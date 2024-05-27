#!/usr/bin/python3
"""
Routes for handling place objects through the API
"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Gets all place objects in a specified city.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Returns a place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a place object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description='Missing user_id')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, description='Missing name')

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
