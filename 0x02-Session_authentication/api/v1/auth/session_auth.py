#!/usr/bin/env python3
""" Module of Session Auth views
"""
import flask
from flask import request
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Session Auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:
        """ User ID for Session ID
        """
        if session_id is None or type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ returns a user based on a cookie value """
        _my_session_id = self.session_cookie(request)
        if not _my_session_id:
            return None
        user_id = self.user_id_for_session_id(_my_session_id)
        if not user_id:
            return None
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """ Deletes user session/logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass
        return True
