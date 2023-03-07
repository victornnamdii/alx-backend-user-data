#!/usr/bin/env python3
"""
API Authentication Class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    API Authentication Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Requires auth
        """
        if not path or not excluded_paths or not len(excluded_paths):
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
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
