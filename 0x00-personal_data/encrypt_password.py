#!/usr/bin/env python3
"""
A module for encrypting passwords
"""
from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password
    """
    return checkpw(password.encode('utf-8'), hashed_password)
