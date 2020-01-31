#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all cities """
    cities = storage.all("City")
    arr_cities = []
    for value in cities.values():
        if value.state_id == state_id:
            arr_cities.append(value.to_dict())

    if len(arr_cities) == 0:
        abort(404)
    return jsonify(arr_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieves the list of all city objects """
    cities = storage.all("City")
    for key, value in cities.items():
        city = key.split(".")
        if city[1] == city_id:
            return jsonify(value.to_dict())
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    """ Deletes a city object """
    cities = storage.all("City")
    for key, value in cities.items():
        city = key.split(".")
        if city[1] == city_id:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City """
    flag = 0
    if request.is_json:
        req = request.get_json()
    else:
        abort(400, "Not a JSON")

    try:
        req["name"]
    except Exception as e:
        abort(400, "Missing name")

    states = storage.all("State")
    for value in states.values():
        if value.id == state_id:
            flag = 1

    if flag:
        req["state_id"] = state_id
    else:
        abort(404)
    new_city = City(**req)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object """
    cities = storage.get("City", city_id)
    if request.is_json:
        req = request.get_json()
    else:
        abort(400, "Not a JSON")

    if cities is None:
        abort(404)
    try:
        req["name"]
    except Exception as e:
        abort(400, "Missing name")

    for key, value in req.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(cities, key, value)
    storage.save()
    return make_response(jsonify(cities.to_dict()), 200)
