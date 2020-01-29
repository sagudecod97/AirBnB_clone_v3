#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.state import State
import copy

@app_views.route('/states/', methods=['GET'])
def get_states():
    states = storage.all("State")
    arr_states = []
    for value in states.values():
        arr_states.append(value.to_dict())
    return jsonify(arr_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    states = storage.all("State")
    for key, value in states.items():
        state = key.split(".")
        if state[1] == state_id:
            return jsonify(value.to_dict())
    return make_response(jsonify({"error":"Not found"}), 404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    states = storage.all("State")
    for key, value in states.items():
        state = key.split(".")
        if state[1] == state_id:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response(jsonify({"error":"Not found"}), 404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    if request.is_json:
        req = request.get_json()
    else:
        return make_response(jsonify({"error":"Not a JSON"}), 400)

    try:
        req["name"]
    except Exception as e:
        return make_response(jsonify({"error":"Missing name"}), 400)

    new_state = State(**req)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get("State", state_id)
    print("STATE: {}".format(state))
    if request.is_json:
        req = request.get_json()
    else:
        return make_response(jsonify({"error":"Not a JSON"}), 400)

    if state is None:
        return make_response(jsonify({"error":"Not found"}), 404)

    copy_state = copy.deepcopy(state)
    copy_state.name = req["name"]
    storage.delete(state)
    storage.save()
    storage.new(copy_state)
    storage.save()
    return make_response(jsonify({"ahah": 69}), 666)
