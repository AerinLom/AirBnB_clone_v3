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
    if city is None:
        abort(404)
    all_places = storage.all('Place')
    city_places = [place_obj.to_dict() for place_obj in all_places.values()
                   if place_obj.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Returns a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a place object
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
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place object
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

    place.save()
    return jsonify(place.to_dict()), 200
