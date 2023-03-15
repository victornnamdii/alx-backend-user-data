#!/usr/bin/env python3
"""
Handling Authorization
"""

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Retruns a salted hash of the input password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    Returns a string uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Hashes the password of a user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(user.email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login details
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session for user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
