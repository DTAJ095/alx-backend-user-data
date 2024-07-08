#!/usr/bin/env python3
""" Module of Basic Auth
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Returns the decoded value of Base64 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64_authorization_header.encode('utf-8').decode('base64')
        except Exception:
            return None
