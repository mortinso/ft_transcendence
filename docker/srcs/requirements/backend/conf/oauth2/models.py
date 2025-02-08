from django.db import models
from django.conf import settings

class Intra42Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    intra42_id = models.BigIntegerField(unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    last_login = models.DateTimeField(null=True)
    