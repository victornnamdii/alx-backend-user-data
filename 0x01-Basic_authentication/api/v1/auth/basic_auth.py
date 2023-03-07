#!/usr/bin/env python3
"""
Basic Authentication class
"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Tuple
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
        except (binascii.Error, AssertionError):
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
            return tuple(decoded_base64_authorization_header.split(':'))
        return (None, None)
