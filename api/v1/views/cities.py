#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City


@app_views.route('/cities/', methods=['GET'], strict_slashes=False)
def get_cities():
    """Retrieves the list of all cities """
    cities = storage.all("City")
    arr_cities = []
    for value in cities.values():
        arr_cities.append(value.to_dict())
    return jsonify(arr_states)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city(state_id):
    """ Retrieves the list of all city objects """


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


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(state_id):
    """Updates a city object """
    cities = storage.get("City", city_id)
    if request.is_json:
        req = request.get_json()
    else:
        abort(400, "Not a JSON")

    if cities is None:
        abort(404)

    for key, value in req.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(cities, key, value)
            storage.save()
            return make_response(jsonify(cities.to_dict()), 200)
