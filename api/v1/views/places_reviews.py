#!/usr/bin/python3
"""
Routes for handling review objects through the api
"""
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Gets all review objects for a place
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Returns a review object
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        return abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a review object
    """
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a review object
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)

    try:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        return abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)

    if 'text' not in data:
        return abort(400, 'Missing text')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a review object
    """
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)

    try:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
    except Exception:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
