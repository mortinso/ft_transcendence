from rest_framework import permissions
from backend.exceptions import NotFoundHTML
from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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


class IsGameOwner(BasePermission):
    """
    Custom permission to allow only the owner of the game to create or edit it.
    """
    def has_permission(self, request, view):
        user_pk = view.kwargs.get("user_pk")
        
        if not request.user.is_authenticated:
            return False
        return request.user.id == user_pk
