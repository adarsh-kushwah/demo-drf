from rest_framework import permissions
from django.shortcuts import get_object_or_404


class ProfilePermission(permissions.BasePermission):
    """
    authenticated user can only access his own profile
    Permission to check whether the user token is same of user in url routes kwargs
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.id == int(view.kwargs["pk"])
