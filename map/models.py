from django.db import models


class ExistingLocations(models.Model):
    name = models.CharField(max_length=225)
    lat = models.DecimalField(decimal_places=15, max_digits=18)
    lng = models.DecimalField(decimal_places=15, max_digits=18)

