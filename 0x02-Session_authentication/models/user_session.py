#!/usr/bin/env python3
"""
Handling User Sessions
"""

from .base import Base


class UserSession(Base):
    """
    Handling User sessions
    """
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
