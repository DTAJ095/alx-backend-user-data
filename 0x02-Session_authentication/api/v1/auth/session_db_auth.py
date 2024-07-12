#!/usr/bin/env python3
""" New authentication class SessionDBAuth """
from api.v1.auth.session_exp_auth import SessionExpAuth
import uuid
from models.user_session import UserSession
from models.base import DATA
import datetime
from datetime import timedelta


class SessionDBAuth(SessionExpAuth):
    """ Database Session """

    def create_session(self, user_id=None):
        """ create and store new instance for user
        session
        """
        if user_id is None:
            return None
        session_id = str(uuid.uuid4())
        if not session_id:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns the User ID by requesting the UserSession
        in the database
        """
        if session_id is None:
            return None
        if 'UserSession' not in DATA:
            return None
        session = UserSession.search({'session_id': session_id})
        if not session:
            return None
        session = session[0]
        if self.session_duration <= 0:
            return self.session.user_id
        created_at = session.created_at
        session_duration = timedelta(seconds=self.session_duration)
        if (created_at + session_duration) < datetime.datetime.now():
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """ destroys the UserSession based on the
        Session ID from the request cookie
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if 'UserSession' not in DATA:
            return False
        session = UserSession.search({'session_id': session_id})
        if not session:
            return False
        session = session[0]
        session.remove()
        return True
