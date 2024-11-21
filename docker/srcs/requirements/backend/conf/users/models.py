from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: move avatars folder elsewhere

def user_avatar_path(instance, filename):
    return f'{instance.id}/{instance.username}'

class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default.jpg')
    friends = models.ManyToManyField('self', symmetrical=False, related_name="friends_set")
    friend_requests = models.ManyToManyField('self', symmetrical=False, related_name="friend_requests_set")
    blocked = models.ManyToManyField('self', symmetrical=False, related_name="banned_set")
    is_online = models.BooleanField(default=True)
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    draws = models.IntegerField(default = 0)
    games_played = models.IntegerField(default = 0)

def __str__(self):
    return self.username