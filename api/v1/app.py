#!/usr/bin/python3
""" App """
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


ipp = Flask(__name__)
app.register_blueprint(app_views)


cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(c):
    """ Closes the session """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ Returns a 404 """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)
