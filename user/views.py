from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework import status

from property.models import Property
from property.serializers import PropertySerializer
from property.permissions import OwnerPermission

from user.serializers import ProfileSerializer
from user.models import UserProfile, Location

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny

# class UserProfileView(CreateModelMixin, GenericAPIView):

#     queryset = UserProfile.objects.all()
#     """
#         format :-
#                 {
#                     "useraddress":{
#                         "street_address": "tesing",
#                         "pincode":452020
#                         },
#                     "username":"testing1",
#                     "first_name": "",
#                 }
#     """

#     def create(self, request, *args, **kwargs):
#         location = get_object_or_404(Location, postal_code=request.data["address"]["pincode"])
#         request.data["address"].update({"location":location.id})
#         profile_serializer = ProfileSerializer(data = request.data)

#         if profile_serializer.is_valid():
#             profile_serializer.save()
#             context = {'status':'registration success'}
#             return Response(context)
#         return Response(profile_serializer.errors)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class ProfileView(viewsets.ViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        elif self.action == "create":
            return [AllowAny()]
        return super(ProfileView, self).get_permissions()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        {
             "useraddress":{
                     "street_address": "tesing",
                     "location" : {"postal_code":"452020"}
                 },
             "username":"testing1",
             "user_type": "owner",
             "first_name": "testing post",
             "gender": "male",
             "phone_number": "1111122222"
         }
        """

        profile_serializer = self.serializer_class(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            data = {"status": "registration success"}
            return Response(data, status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(UserProfile, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(UserProfile, pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {"message": "user updated successfully"}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(UserProfile, pk=pk)
        user.delete()
        data = {"status": "user deleted successfully"}
        return Response(data, status=status.HTTP_200_OK)
