from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from property.models import Property


class OwnerPermission(permissions.BasePermission):
    message = "Permission denied"

    def has_permission(self, request, view):
        property = Property.objects.select_related('owner').get(pk=view.kwargs['pk'])
        return request.user.id == property.owner.id