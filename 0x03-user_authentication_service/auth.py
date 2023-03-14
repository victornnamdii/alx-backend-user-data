#!/usr/bin/env python3
"""
Handling Authorization
"""

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    Retruns a salted hash of the input password
    """
    return hashpw(password.encode('utf-8'), gensalt())
