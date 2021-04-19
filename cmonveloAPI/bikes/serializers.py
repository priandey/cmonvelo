from rest_framework import serializers
from .models import Owner, Bike, FoundAlert, Trait


class TraitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trait
        fields = ['name']


class FoundAlertSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d/%m/%y à %Hh%M", read_only=True)
    bike = serializers.HiddenField(default=0)

    class Meta:
        model = FoundAlert
        fields = ['message', 'coords', 'bike', 'date']
        read_only_fields = ['date',]


class BikeOwnerSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    alerts = FoundAlertSerializer(many=True, read_only=True)
    traits = serializers.PrimaryKeyRelatedField(queryset=Trait.objects.all(), many=True, allow_empty=True, allow_null=True)

    class Meta:
        model = Bike
        fields = ['name', 'picture', 'reference', 'traits', 'robbed', 'robbed_location', 'pk', 'owner', 'alerts']
        read_only_fields = ['pk', 'owner', 'alerts']


class BikePublicSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=0)
    name = serializers.CharField(write_only=True, allow_blank=True)
    traits = TraitSerializer(many=True, required=False)
    date_of_robbery = serializers.DateTimeField(format="%x %X", read_only=True)

    class Meta:
        model = Bike
        fields = ['name', 'picture', 'reference', 'traits', 'robbed', 'robbed_location', 'date_of_robbery', 'pk', 'owner']
        read_only_fields = ['pk',]
