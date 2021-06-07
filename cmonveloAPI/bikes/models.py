import requests

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Owner(AbstractUser):
    username = models.CharField(max_length=80, blank=True)
    email = models.EmailField(unique=True)
    is_institution = models.BooleanField(default=False)
    is_moderation = models.BooleanField(default=False)
    geographic_zone = models.CharField(max_length=255, null=True, blank=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    @property
    def geo_zones(self):
        if self.is_institution:
            return self.geographic_zone.split(',')
        else:
            return "Cet utilisateur n'est pas une institution"


class Trait(models.Model):
    name = models.CharField(max_length=50, unique=True, primary_key=True)


class Bike(models.Model):
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name="bikes")
    traits = models.ManyToManyField(Trait, related_name="bikes", blank=True)
    robbed = models.BooleanField(default=False, null=False)
    reference = models.CharField(max_length=255, unique=True)
    picture = models.ImageField(upload_to="bikes/", null=True, default="bikes/default.jpg", max_length=255)
    robbed_location = models.JSONField(null=True, blank=True)
    date_of_robbery = models.DateTimeField(null=True)
    robbery_city = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            place = requests.get("https://api-adresse.data.gouv.fr/reverse/", params={
                "lon": self.robbed_location['longitude'],
                "lat": self.robbed_location['latitude'],
            }).json()
            if len(place['features']) > 0:
                self.robbery_city = place['features'][0]['properties']['city']
        except KeyError:
            pass
        super(Bike, self).save(*args, **kwargs)

    def __str__(self):
        return self.reference

    def set_robbery_date(self):
        """
        Set a date for the robbery declaration.
        """
        self.date_of_robbery = timezone.now()
        self.save()


class FoundAlert(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name="alerts", blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    coords = models.JSONField()


class ModerationToken(models.Model):
    token = models.CharField(max_length=255)
