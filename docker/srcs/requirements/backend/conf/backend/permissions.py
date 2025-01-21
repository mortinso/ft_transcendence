from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    Global permission check if user is accessing his own data.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
