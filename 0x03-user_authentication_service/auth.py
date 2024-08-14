#!/usr/bin/env python3
""" Auth Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


def _hash_password(password: str) -> str:
    """Hashes a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a random UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            self._db.add_user(email, hashed_password)

        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validate email and password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """Create a new session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        new_session_id = _generate_uuid()
        user.session_id = new_session_id
        return new_session_id
