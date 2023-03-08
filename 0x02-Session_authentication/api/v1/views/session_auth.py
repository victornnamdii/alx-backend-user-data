#!/usr/bin/env python3
"""
Session Authentication
"""

from api.v1.views import app_views
from flask import jsonify, request
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles session authentication
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})[0]
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401
    except (KeyError, IndexError):
        return jsonify({"error": "no user found for this email"}), 404
