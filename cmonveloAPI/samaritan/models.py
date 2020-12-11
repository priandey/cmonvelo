from django.db import models

class FoundAlert(models.Model):
    bike = models.ForeignKey('bikeowner.Bike', on_delete=models.CASCADE, related_name="alerts", blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    coords = models.JSONField()
