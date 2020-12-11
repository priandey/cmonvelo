from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import secrets


class Owner(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    username = models.CharField(max_length=80, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'phone'


class Bike(models.Model):
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name="bikes")
    name = models.CharField(max_length=100, null=False, blank=False)
    robbed = models.BooleanField(default=False, null=False)
    reference = models.CharField(max_length=255, unique=True)
    picture = models.ImageField(upload_to="bikes/", null=True, default="bikes/default.jpg", max_length=255)
    robbed_location = models.JSONField(null=True)
    date_of_robbery = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def set_robbery_date(self):
        """
        Set a date for the robbery declaration. First iteration is just for now
        """
        self.date_of_robbery = timezone.now()
        self.save()


class Details(models.Model):
    bike = models.OneToOneField('Bike', on_delete=models.CASCADE, primary_key=True, verbose_name="details")
    color_major = models.CharField(max_length=255)
    color_minor = models.CharField(max_length=255)
    frame_shape = models.CharField(max_length=255)
    handlebar_shape = models.CharField(max_length=255)
    small_detail_1 = models.CharField(max_length=255)
    small_detail_2 = models.CharField(max_length=255)
    brand = models.ForeignKey('Details', on_delete=models.SET_NULL, verbose_name="bikes", null=True)


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)

    def __repr__(self):
        return self.name
