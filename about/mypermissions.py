from rest_framework.permissions import BasePermission
import os

class SecretWordPermission(BasePermission):
    """
    Custom permission to allow access if the correct secret word is provided in headers.
    """

    SECRET_PASSWORD = os.getenv("SECRET_KEYWORD", "ronaldo")  # Use env variable for security

    def has_permission(self, request, view):
        # Get the provided secret key from headers
        provided_password = request.headers.get("X-Secret-Key")

        # Check if the provided secret key matches the expected one
        if provided_password == self.SECRET_PASSWORD:
            return True

        return False  # Deny access if no match
