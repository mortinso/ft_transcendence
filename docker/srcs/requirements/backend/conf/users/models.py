from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.CharField(max_length=240,blank=True)
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    draws = models.IntegerField(default = 0)
    games_played = models.IntegerField(default = 0)

def __string__(self):
    return self.username