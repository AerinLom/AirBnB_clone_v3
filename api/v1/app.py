#!/usr/bin/python3
"""
This script initializes a Flask application for an API
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def no_page_exists(error):
    """
    Returns a 404 response
    """
    error_response = {"error": "Not found"}
    return jsonify(error_response), 404


if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
