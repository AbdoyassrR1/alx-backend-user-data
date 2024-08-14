#!/usr/bin/env python3
""" Auth Module"""
import bcrypt


def _hash_password(password: str) -> str:
    """Hashes a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
