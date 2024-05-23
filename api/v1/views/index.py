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
