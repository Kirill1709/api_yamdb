from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.is_admin
        return False


class IsAutrhOrAdminOrModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.author == request.user
                or request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_authenticated
                and request.user.role == 'moderator')
