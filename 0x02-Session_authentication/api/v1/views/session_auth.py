#!/usr/bin/env python3
""" Flask view that handles all routes for
the session authentication
"""
import flask
from flask import abort, jsonify, request
import os
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def user_auth_session_login():
    """ Handles user login authentication """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user_id=user.id)
        cookie_name = os.getenv('SESSION_NAME')
        response = jsonify(user.to_json())
        response.set_cookie(cookie_name, session_id)
        return response
    else:
        return jsonify({"error": "wrong password"}), 401
