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
    if request.method == 'GET':
        stats = {}
        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in PLURALS.items():
            stats[value] = storage.count(key)
        return jsonify(stats)
