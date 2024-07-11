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
    try:
        user = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"})
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        SESSION_NAME = os.getenv('SESSION_NAME')
        response.set_cookie(SESSION_NAME, session_id)
        return response
