#!/usr/bin/env python3
"""
SessionDBAuth Class
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Storing sessions in a database
    """
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession
        and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession
        in the database based on session_id
        """
        try:
            session = UserSession.search({'session_id': session_id})[0]
            if self.session_duration <= 0:
                return session.user_id
            duration = timedelta(seconds=self.session_duration)
            assert ((session.created_at + duration) > datetime.utcnow())
            return session.user_id
        except (KeyError, IndexError, AssertionError):
            return None

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID
        from the request cookie
        """
        session_id = self.session_cookie(request)
        try:
            session = UserSession.search({'session_id': session_id})[0]
            session.remove()
            return True
        except (KeyError, IndexError):
            return False
