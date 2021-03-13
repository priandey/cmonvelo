from rest_framework import serializers
from bikeowner.models import Bike, Details
from .models import FoundAlert


class BikePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['robbed', 'reference', 'robbed_location', 'details', 'picture']  # TODO : Useless 'robbed'
        read_only_fields = ['robbed', 'reference', 'robbed_location', 'details', 'picture']


class FoundAlertSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d/%m/%y à %Hh%M", read_only=True)
    class Meta:
        model = FoundAlert
        fields = ['message', 'coords', 'bike', 'date']
        read_only_fields = ['date',]