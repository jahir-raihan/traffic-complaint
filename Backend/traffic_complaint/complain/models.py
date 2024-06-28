from django.db import models


class PoliceStation(models.Model):
    station_name = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    division = models.CharField(max_length=40)
    area = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.station_name} of {self.city}'

