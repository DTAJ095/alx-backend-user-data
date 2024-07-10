#!/usr/bin/env python3
""" Module of Auth views
"""
import flask
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        for i in excluded_paths:
            if i[-1] == '*':
                if path.startswith(i[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        _my_session_id = request.cookies.get(cookie_name)
        return _my_session_id
