from django.db import models

# Create your models here.
class Bus(models.Model):
    bus_number = models.CharField(max_length=20)
    time = models.TimeField()
    destination = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.bus_number