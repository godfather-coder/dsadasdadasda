from django.db import models
from django.conf import settings

class Listing(models.Model):
    listing_id = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.listing_id
