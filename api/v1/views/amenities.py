#!/usr/bin/python3
""" Amenity """
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State
from models.amenity import Amenity
import copy


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all amenities """
    amenities = storage.all("Amenity")
    arr_amenities = []
    for value in amenities.values():
        arr_amenities.append(value.to_dict())
    return jsonify(arr_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an amenity object """
    amenities = storage.all("Amenity")
    for key, value in amenities.items():
        amenity = key.split(".")
        if amenity[1] == amenity_id:
            print(value.to_dict())
            return jsonify(value.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenities = storage.all("Amenity")
    for key, value in amenities.items():
        amenity = key.split(".")
        if amenity[1] == amenity_id:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity """
    if request.is_json:
        req = request.get_json()
    else:
        abort(400, "Not a JSON")

    try:
        req["name"]
    except Exception as e:
        abort(400, "Missing name")

    new_amenity = Amenity(**req)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an amenity """
    amenity = storage.get("Amenity", amenity_id)
    if request.is_json:
        req = request.get_json()
    else:
        abort(400, "Not a JSON")

    if amenity is None:
        abort(404)

    for key, value in req.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
