from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework import serializers

from user.models import UserProfile, UserAddress, Location


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)


class LocationSerializer(serializers.Serializer):
    postal_code = serializers.CharField(max_length=6)

    def validate_postal_code(self, value):
        try:
            return Location.objects.get(postal_code=value)
        except Location.DoesNotExist:
            raise serializers.ValidationError("Postal code not exists.")


class AddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = UserAddress
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}


class ProfileSerializer(serializers.ModelSerializer):
    useraddress = AddressSerializer()
    
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "useraddress",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "gender",
            "phone_number",
            "profile_picture",
        ]

    def validate_phone_number(self, value):
        if value.isdigit() and len(value) == 10:
            return value
        raise serializers.ValidationError("Phone number must be of 10 digits.")

    def create(self, validated_data):
        address_data = validated_data.pop("useraddress")
        location = address_data.pop("location")["postal_code"]
        user = UserProfile.objects.create(**validated_data)
        address = UserAddress.objects.create(
            user=user, location=location, **address_data
        )
        return user

    def update(self, user_instance, validated_data):
        address_data = validated_data.pop("useraddress", None)

        if address_data:
            user_address = user_instance.useraddress
            user_address.street_address = address_data.get(
                "street_address", user_address.street_address
            )

            if "location" in address_data and "postal_code" in address_data["location"]:
                location = address_data["location"]["postal_code"]
                user_address.location = location
            user_address.save()
        for key, value in validated_data.items():
            setattr(user_instance, key, value)
        user_instance.save()
        return user_instance
