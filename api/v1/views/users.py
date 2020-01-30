#!/usr/bin/python3
""" User """
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User
import copy


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all users """
    users = storage.all("User")
    arr_users = []
    for value in users.values():
        arr_users.append(value.to_dict())
    return jsonify(arr_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id):
    """Retrieves an user object """
    users = storage.all("User")
    arr_users = []
    for key, value in users.items():
        user = key.split(".")
        if user[1] == user_id:
            print(value.to_dict())
            return jsonify(value.to_dict())
    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id):
    """Delete an user object """
    users = storage.all("User")
    for key, value in users.items():
        user = key.split(".")
    if user[1] == user_id:
        storage.delete(value)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a user """
    if request.is_json:
        req = request.get_json()
    else:
        abort(400, "Not a JSON")

    try:
        req["email"]
    except Exception as e:
        abort(400, "Missing email")

    try:
        req["password"]
    except Exception as e:
        abort(400, "Missing password")

    new_user = User(**req)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a user """
    users = storage.get("User", user_id)
    if request.is_json:
        req = request.get_json()
    else:
        abort(400, "Not a JSON")

    if users is None:
        abort(404)

    for key, value in req.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(users, key, value)
        storage.save()
        return make_response(jsonify(users.to_dict()), 200)
