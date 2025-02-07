from django.db import models

# Create your models here.

class intra42User(models.Model):
	id = models.BigIntegerField(primary_key=True, default=0)
	email = models.EmailField(unique=True, blank=True, null=True)
	avatar = models.URLField(blank=True, null=True)
	login = models.CharField(max_length=100, blank=True, null=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	url = models.URLField(blank=True, null=True)
	last_login = models.DateTimeField()