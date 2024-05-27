#!/usr/bin/python3
"""
view that handles API actions to link Place objects and Amenity objects
"""
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def fetch_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_object = [amenity.to_dict() for amenity in place.amenities]
    else:
        place_object = [storage.get(Amenity, amenity_id).to_dict()
                        for amenity_id in place.amenity_ids]
    return jsonify(place_object)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for object_amenity in place.amenities:
        if object_amenity.id == amenity.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def connect_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            place.amenities.append(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
