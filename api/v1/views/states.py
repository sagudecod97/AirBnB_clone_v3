#!/usr/bin/python3
""" State """
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State
import copy


@app_views.route('/states/', methods=['GET'])
def get_states():
    """ Retrieves the list of all state """
    states = storage.all("State")
    arr_states = []
    for value in states.values():
        arr_states.append(value.to_dict())
    return jsonify(arr_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a state object """
    states = storage.all("State")
    for key, value in states.items():
        state = key.split(".")
        if state[1] == state_id:
            return jsonify(value.to_dict())
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a state object """
    states = storage.all("State")
    for key, value in states.items():
        state = key.split(".")
        if state[1] == state_id:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ Creates a state object """
    if request.is_json:
        req = request.get_json()
        print("json")
    else:
        abort(400, "Not a JSON")

    try:
        req["name"]
    except Exception as e:
        abort(400, "Missing name")

    new_state = State(**req)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state object """
    state = storage.get("State", state_id)
    print("STATE: {}".format(state))
    if request.is_json:
        req = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if state is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    copy_state = copy.deepcopy(state)
    copy_state.name = req["name"]
    storage.delete(state)
    storage.save()
    storage.new(copy_state)
    storage.save()
    return make_response(jsonify({"ahah": 69}), 666)
