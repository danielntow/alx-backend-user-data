#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import TypeVar, List
User = TypeVar('User')


class Auth:
    """
    A class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the path requires authentication

        Args:
            path (str): The path to check
            excluded_paths (List[str]): A list of paths that are excluded from authentication

        Returns:
            bool: True if the path requires authentication, False otherwise
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path to ensure consistency
        if path[-1] != "/":
            path += "/"

        for excluded_path in excluded_paths:
            # Normalize the excluded path to ensure consistency
            if excluded_path[-1] != "/":
                excluded_path += "/"

            # Check if the excluded path ends with a wildcard "*"
            if excluded_path.endswith("*"):
                # Match any path that starts with the base of the excluded path
                base_excluded_path = excluded_path[:-1]
                if path.startswith(base_excluded_path):
                    return False
            else:
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request

        Args:
            request: The Flask request object

        Returns:
            str: The value of the Authorization header, or None if not present
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request

        Args:
            request: The Flask request object

        Returns:
            User: The current user, or None if not found
        """
        return None
