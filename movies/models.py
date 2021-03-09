from django.db import models

# Create your models here.


class PopCorner(models.Model):
    objects = None
    text = models.TextField()
    image_url = models.TextField()
