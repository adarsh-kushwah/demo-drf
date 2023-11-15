from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


# class OwnerPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         token = get_object_or_404(Token, key=request.auth)
#         return request.user == token.user