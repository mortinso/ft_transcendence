from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.CharField(max_length=240,blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, related_name="friends_set")
    friend_requests = models.ManyToManyField('self', symmetrical=False, related_name="friend_requests_set")
    banned = models.ManyToManyField('self', symmetrical=False, related_name="banned_set")
    muted = models.ManyToManyField('self', symmetrical=False, related_name="muted_set")
    is_online = models.BooleanField(default=True)
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    draws = models.IntegerField(default = 0)
    games_played = models.IntegerField(default = 0)

def __str__(self):
    return self.username