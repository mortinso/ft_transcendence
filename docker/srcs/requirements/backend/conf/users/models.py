from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
import os

def user_avatar_path(instance, filename):
    # Extract the file extension
    ext = filename.split('.')[-1]
    
    return f'{instance.id}/user_{instance.id}.{ext}'

class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, default='default.jpg')
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends_set')
    friend_requests = models.ManyToManyField('self', symmetrical=False, related_name='friend_requests_set')
    blocked = models.ManyToManyField('self', symmetrical=False, related_name='banned_set')
    is_online = models.BooleanField(default=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Check if there is an existing file and delete it
        try:
            this = User.objects.get(id=self.id)
            if this.avatar and this.avatar.name != 'default.jpg':
                # Delete the existing file using default_storage
                if default_storage.exists(this.avatar.name):
                    default_storage.delete(this.avatar.name)
        except User.DoesNotExist:
            pass  # This is a new user, so no need to delete anything

        super(User, self).save(*args, **kwargs)