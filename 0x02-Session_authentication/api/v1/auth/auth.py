#!/usr/bin/env python3
"""
API Authentication Class
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    API Authentication Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Requires auth
        """
        if path and excluded_paths:
            for excluded_path in excluded_paths:
                if '*' in excluded_path[-2:]:
                    excluded_path = excluded_path.split('*')[0]
                if excluded_path in path or excluded_path in path + '/':
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current User
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if request:
            _my_session_id = getenv('SESSION_NAME')
            return request.cookies.get(_my_session_id, None)
        return None
