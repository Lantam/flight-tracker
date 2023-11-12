from django.db import models


class Api(models.Model):
    registration_number = models.CharField(max_length=10, unique=True)
    country_code = models.CharField(max_length=2, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    elevation = models.IntegerField(null=True)
    head_direction = models.IntegerField(null=True)
    airline_icao = models.CharField(max_length=3, null=True)
    aircraft_icao = models.CharField(max_length=4, null=True)
    departure_icao = models.CharField(max_length=4, null=True)
    arrival_icao = models.CharField(max_length=4, null=True)
    status = models.CharField(max_length=20, null=True)


class Search(models.Model):
    location = models.TextField(null=True)

    def __str__(self):
        return self.location
