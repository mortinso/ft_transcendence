from rest_framework import permissions
from backend.exceptions import NotFoundHTML

class IsSelf(permissions.BasePermission):
    """
    Global permission check if user is accessing his own data.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

class IsAuthenticatedOrNotFound(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        raise NotFoundHTML(detail="Not found.")