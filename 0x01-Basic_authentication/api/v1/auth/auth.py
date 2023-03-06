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
        return False

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current User
        """
        return None
