#!/usr/bin/env python3
""" Session expiration module """
from api.v1.auth.session_auth import SessionAuth
import os
import datetime
from datetime import timedelta


class SessionExpAuth(SessionAuth):
    """ Session expiration class """
    session_dict = {}

    def __init__(self):
        """ Initialize the class """
        session_duration = os.getenv('SESSION_DURATION')
        try:
            if not session_duration:
                session_duration = 0
            session_duration = int(session_duration)
        except ValueError:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """ create a new session ID """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.session_dict['user_id'] = user_id
        self.session_dict['created_at'] = datetime.datetime.now()
        self.user_id_by_session_id[session_id] = self.session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return user_id from the session dictionary """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.session_dict.get('user_id')
        if not self.session_dict['created_at']:
            return None
        created_at = self.session_dict['created_at']
        session_duration = timedelta(seconds=self.session_duration)
        if (created_at + session_duration) < datetime.datetime.now():
            return None
        return self.session_dict.get('user_id')
