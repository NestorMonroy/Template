
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # anybody can do GET, HEAD, or OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # only an unauthenticated user can do POST, PUT, PATCH, DELETE
        user = request.user
        return not user.is_authenticated


