#!/usr/bin/python3
"""
Module defines a view that handles API actions for the State objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects.
    """
    all_state = storage.all(State).values()
    return jsonify([state.to_dict() for state in all_state])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieves a State object by id.
    """
    filtered_state = storage.get(State, state_id)
    if not filtered_state:
        abort(404)
    return jsonify(filtered_state.to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_state_by_id(state_id):
    """
    Deletes a State object.
    """
    state_to_delete = storage.get(State, state_id)
    if not state_to_delete:
        abort(404)
    storage.delete(state_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    """
    Creates a State object.
    """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, description="Missing name")

    created_state = State(**data)
    storage.new(created_state)
    storage.save()
    return jsonify(created_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.
    """
    state_to_update = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state_to_update, key, value)
    storage.save()
    return jsonify(state_to_update.to_dict()), 200
