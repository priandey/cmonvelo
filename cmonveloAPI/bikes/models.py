from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Owner(AbstractUser):
    username = models.CharField(max_length=80, blank=True)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'


class Trait(models.Model):
    name = models.CharField(max_length=50, unique=True, primary_key=True)


class Bike(models.Model):
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name="bikes")
    traits = models.ManyToManyField(Trait, related_name="bikes", blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    robbed = models.BooleanField(default=False, null=False)
    reference = models.CharField(max_length=255, unique=True)
    picture = models.ImageField(upload_to="bikes/", null=True, default="bikes/default.jpg", max_length=255)
    robbed_location = models.JSONField(null=True, blank=True)
    date_of_robbery = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.name

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
