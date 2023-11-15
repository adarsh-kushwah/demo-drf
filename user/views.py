from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from property.models import Property
from property.serializers import PropertySerializer


class ProfileView(APIView):

    def get(self, request, *args, **kwargs):
        return Response('test')
