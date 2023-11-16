from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import mixins
from rest_framework.generics import RetrieveAPIView

from property.models import Property
from property.serializers import PropertySerializer
from property.permissions import OwnerPermission


class PropertyView(APIView):
    
    def get(self, request, *args, **kwargs):
        property = Property.objects.all()
        property_serializer = PropertySerializer(
            property, many=True, context={"request": request}
        )
        content = {"user": request.user.username, "property": property_serializer.data}
        return Response(content)

    def post(self, request, *args, **kwargs):
        data = request.data
        data["owner"] = reverse(
            "userprofile-detail", kwargs={"pk": request.data["owner"]}, request=request
        )
        property_serializer = PropertySerializer(data=data)
        if property_serializer.is_valid():
            
            return Response({'status':'success'})
        else:
            content = {"errors": property_serializer.errors}
            return Response(content)


class PropertyDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, OwnerPermission]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
