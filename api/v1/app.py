#!/usr/bin/python3
""" App """
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(c):
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is None:
        host = "0.0.0.0"
    else:
        host = getenv('HBNB_API_HOST')

    if getenv('HBNB_API_PORT') is None:
        port = "5000"
    else:
        port = getenv('HBNB_API_PORT')
        app.run(host=host, port=port, threaded=True, debug=True)
