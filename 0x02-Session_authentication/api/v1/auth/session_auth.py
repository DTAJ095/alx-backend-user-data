#!/usr/bin/env python3
""" Module of Session Auth views
"""
import flask
from flask import request
from api.v1.auth.auth import Auth
import uuid


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
