#!/usr/bin/env python3
"""
Session Expiration
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    Handling session expiration
    """
    def __init__(self) -> None:
        """
        Initializing session duration
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except KeyError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        try:
            assert (isinstance(session_id, str))
            session_dictionary = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dictionary['user_id']
            created_at = session_dictionary['created_at']
            duration = timedelta(seconds=self.session_duration)
            assert ((created_at + duration) > datetime.now())
            return session_dictionary['user_id']
        except (AssertionError, KeyError):
            return None
