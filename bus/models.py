from django.db import models


class Bus(models.Model):

    bus_number = models.CharField(max_length=20)

    time = models.TimeField()

    destination = models.CharField(max_length=200)

    latitude = models.FloatField(default=0)

    longitude = models.FloatField(default=0)

    # GPS last updated time
    location_updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # GPS currently running or not
    gps_active = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.bus_number