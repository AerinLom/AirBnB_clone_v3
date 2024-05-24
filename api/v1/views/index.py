#!/usr/bin/python3
"""
Module defines a Flask route that returns  JSON status response
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Route to check the status of the API
    """
    resp = {"status": "OK"}
    return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of objects by type.
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
