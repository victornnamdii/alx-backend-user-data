#!/usr/bin/env python3
"""
Basic Authentication class
"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Tuple, TypeVar
from models.user import User
import binascii


class BasicAuth(Auth):
    """
    Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header for a Basic
        Authentication
        """
        if isinstance(authorization_header, str) and\
                authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        try:
            assert (isinstance(base64_authorization_header, str))
            string = b64decode(base64_authorization_header, validate=True)
            string = string.decode('utf-8')
            return string
        except (binascii.Error, AssertionError, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """
        Returns the user email and password from the Base64 decoded value
        """
        if isinstance(decoded_base64_authorization_header, str) and\
                ':' in decoded_base64_authorization_header:
            credentials = decoded_base64_authorization_header.split(':')
            if len(credentials) > 2:
                for i in range(2, len(credentials)):
                    if credentials[i] == '':
                        credentials[1] = credentials[1] + ':'
                        continue
                    credentials[1] = credentials[1] + ':' + credentials[i]
            return (credentials[0], credentials[1])
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password
        """
        try:
            assert (isinstance(user_email, str) and isinstance(user_pwd, str))
            user = User.search({'email': user_email})[0]
            if user.is_valid_password(user_pwd):
                return user
        except (AssertionError, KeyError, IndexError):
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_email, user_pwd)
