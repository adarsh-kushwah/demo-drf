from rest_framework import serializers

from property.models import Property


class PropertySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="property-detail", lookup_field="pk"
    )

    class Meta:
        model = Property
        fields = "__all__"
