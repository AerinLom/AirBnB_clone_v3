#!/usr/bin/python3
"""
route for handling amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """
    retrieves all Amenity objects
    """
    all_amenities = storage.all(Amenity).values
    return jsonify([all_amenities.to_dict() for amenity in all_amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieves an Amenity object by id.
    """
    filtered_amenity = storage.get(Amenity, amenity_id)
    if not filtered_amenity:
        abort(404)
    return jsonify(filtered_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Deletes an Amenity object.
    """
    amenity_to_delete = storage.get(Amenity, amenity_id)
    if not amenity_to_delete:
        abort(404)
    storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """
    Creates an Amenity object.
    """
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if data.get("name") is None:
        abort(400, description="Missing name")

    created_amenity = Amenity(**data)
    storage.new(created_amenity)
    storage.save()
    return jsonify(created_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',  methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """
    Update amenity by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if amenity:
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
