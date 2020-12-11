from rest_framework import serializers
from .models import Owner, Bike, Details
from samaritan.serializers import FoundAlertSerializer


class OwnerSerializer(serializers.ModelSerializer):
    bikes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ['phone', 'username', 'email', 'bikes']


class BikeOwnerSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(many=False, read_only=True)
    alerts = FoundAlertSerializer(many=True, read_only=True)
    picture = serializers.ImageField(allow_null=True, use_url=False)

    class Meta:
        model = Bike
        fields = ['name', 'picture', 'reference', 'robbed', 'robbed_location', 'pk', 'owner', 'alerts']
