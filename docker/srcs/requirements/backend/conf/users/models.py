from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
import os
import datetime
from django.core.cache import cache
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def user_avatar_path(instance, filename):
    # Extract the file extension
    ext = filename.split('.')[-1]
    
    return f'{instance.id}/user_{instance.id}.{ext}'

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path, default='default.jpg')
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends_set')
    friend_requests = models.ManyToManyField('self', symmetrical=False, related_name='friend_requests_set')
    blocked = models.ManyToManyField('self', symmetrical=False, related_name='banned_set')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    tfa = models.BooleanField(default=False)
    otp = models.CharField(max_length=64, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)

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
            pass

        super(User, self).save(*args, **kwargs)
    
    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def online(self):
        logger.debug(f"{self.username} last_seen is: {self.last_seen()}")
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 
