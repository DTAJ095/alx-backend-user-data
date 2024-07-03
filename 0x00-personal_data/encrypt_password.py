#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt


def hash_password(password: str) -> str:
    """ Returns a hashed password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: str, password: str) -> bool:
    """ Validate a password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
