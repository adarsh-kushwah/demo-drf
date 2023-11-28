from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import mixins, status as status_codes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import permission_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes

from property.models import Property
from property.serializers import PropertySerializer
from property.permissions import OwnerPermission
from property.utility import fully_qualified_URL


class PropertyView(APIView):

    @throttle_classes([UserRateThrottle])
    def get(self, request, *args, **kwargs):
        """
        showing all properties to annonomous user
        """
        property = Property.objects.all()
        property_serializer = PropertySerializer(
            property, many=True, context={"request": request}
        )
        data = {"user": request.user.username, "property": property_serializer.data}
        return Response(data, status=status_codes.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        data = request.data
        data["owner"] = fully_qualified_URL("userprofile-detail", request)
        property_serializer = PropertySerializer(data=data)

        if property_serializer.is_valid():
            property_serializer.save()
            data = {"message": "success"}
            status = status_codes.HTTP_201_CREATED
        else:
            data = {"errors": property_serializer.errors}
            status = status_codes.HTTP_400_BAD_REQUEST

        return Response(data, status=status)


class PropertyDetailView(GenericAPIView,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin ):

    permission_classes = [IsAuthenticated, OwnerPermission]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

    #caching result for 30 seconds
    @method_decorator(cache_page(30))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)