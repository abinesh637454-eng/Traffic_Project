from django.db import models


class TrafficRecord(models.Model):
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=128)
    vehicle_count = models.IntegerField()
    vehicle_type = models.CharField(max_length=64)
    weather = models.CharField(max_length=64)
    road_condition = models.CharField(max_length=64)
    hour = models.IntegerField()

    class Meta:
        verbose_name = "Traffic Record"
        verbose_name_plural = "Traffic Records"

    def __str__(self):
        return f"{self.date} {self.time} {self.location}"
