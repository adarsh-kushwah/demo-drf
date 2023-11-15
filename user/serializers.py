from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)