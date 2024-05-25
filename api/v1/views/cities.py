#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False)
def get_city_by_id(city_id):
    """
    gets a city
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """
    deletes a city
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
)
def create_city(state_id):
    """
    creates a city
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id

    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>",  methods=["PUT"],
                 strict_slashes=False)
def city_update(city_id):
    """
    update city by id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if city:
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
