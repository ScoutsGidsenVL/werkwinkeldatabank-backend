from rest_framework import permissions


class CustomDjangoPermission(permissions.BasePermission):
    permission_name = None
    message = "You are not authorized to access this route."

    def __init__(self, permission_name):
        self.permission_name = permission_name

    def has_permission(self, request, view):
        return request.user.has_perm(self.permission_name)
