#!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, jsonify, request, abort
from sqlalchemy.orm.exc import NoResultFound
from typing import Union, Tuple
from auth import Auth
from db import DB


app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """
    Home Page
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> Union[str, Tuple]:
    """
    Return users
    """
    email, password = request.form.get('email'), request.form.get('password')
    try:
        auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Handles log-in
    """
    email, password = request.form.get('email'), request.form.get('password')
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
