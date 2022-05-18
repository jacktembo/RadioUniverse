from django.db import models
from .utils import countries
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Automatically create authentication token when a user object is created.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Token.objects.create(user=instance)


class RadioStation(models.Model):
    """
    A radio station with all it's details.
    """
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, choices=countries, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    banner_image_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=100, default='English')

    def __str__(self):
        """
        string representation of the objects.
        :return:
        """
        return self.name
