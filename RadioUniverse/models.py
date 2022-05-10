from django.db import models
from .utils import countries


class RadioStation(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, choices=countries, blank=True, null=True)
    town = models.CharField(max_length=100, default='Lusaka')
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    banner_image_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=100, default='English')


    def __str__(self):
        return self.name
