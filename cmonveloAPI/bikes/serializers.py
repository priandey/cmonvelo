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
    alerts = FoundAlertSerializer(many=True, read_only=True, label="Signalement")
    traits = serializers.PrimaryKeyRelatedField(queryset=Trait.objects.all(), many=True, label="Caractéristiques")
    owner = serializers.StringRelatedField(label="Propriétaire")
    picture = serializers.ImageField(max_length=None, allow_empty_file=True, label="Image", required=False, allow_null=True)

    class Meta:
        model = Bike
        fields = [
            'reference',
            'owner',
            'robbery_city',
            'picture',
            'traits',
            'robbed',
            'date_of_robbery',
            'robbed_location',
            'pk',
            'alerts',
            'circumstances',
        ]

        read_only_fields = ['pk', 'owner', 'alerts', 'robbery_city']
        extra_kwargs = {
            'reference': {'label':'Référence'},
            'robbery_city': {'label':'Ville du vol'},
            'date_of_robbery': {'label':'Date du vol'},
            'robbed': {'label':'Encore déclaré volé'},
            'robbed_location': {'label':'Coordonnées du vol'},
        }


class BikePublicSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=0)
    traits = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    date_of_robbery = serializers.DateTimeField(format="%d/%m/%y %Hh")
    picture = serializers.ImageField(max_length=None, allow_empty_file=True, required=False, allow_null=True)

    class Meta:
        model = Bike
        fields = [
            'picture',
            'reference',
            'traits',
            'robbed',
            'robbed_location',
            'robbery_city',
            'date_of_robbery',
            'pk',
            'owner',
            "circumstances",
        ]
        read_only_fields = ['pk', 'robbery_city']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['email', 'is_moderation', 'is_institution', 'is_staff', 'geographic_zone']
