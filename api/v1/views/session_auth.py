#!/usr/bin/env python3

"""
Session Authentication Views
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Log in using session authentication
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')

    if not user_email:
        return jsonify(error="email missing"), 400
    if not user_pwd:
        return jsonify(error="password missing"), 400

    users = User.search({"email": user_email})
    if not users:
        return jsonify(error="no user found for this email"), 404

    for user in users:
        if user.is_valid_password(user_pwd):
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify(error="wrong password"), 401

    return jsonify(error="no user found for this email"), 404


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Log out using session authentication
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200


def see():
    pass
