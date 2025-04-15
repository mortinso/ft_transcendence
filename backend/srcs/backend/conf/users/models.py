from django.db import models
from django.contrib.auth.models import AbstractUser
from games.models import Game
from django.core.files.storage import default_storage
import os
from django.core.cache import cache
from django.conf import settings
import uuid
import logging
import datetime
from django.utils import timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def user_avatar_path(instance, filename):
    # Extract the file extension
    ext = filename.split(".")[-1]

    return f"{instance.id}/avatar.{ext}"


IDIOMS = (
    ("EN", "EN"),
    ("ES", "ES"),
    ("PT", "PT"),
)



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path, default="default.jpg")
    friends = models.ManyToManyField("self", symmetrical=False, related_name="friends_set")
    friend_requests = models.ManyToManyField("self", symmetrical=False, related_name="friend_requests_set")
    blocked = models.ManyToManyField("self", symmetrical=False, related_name="blocked_set")
    # pong_requests = models.ManyToManyField("self", symmetrical=False, related_name="pong_requests_set")
    # ttt_requests = models.ManyToManyField("self", symmetrical=False, related_name="ttt_requests_set")
    game_list = models.ManyToManyField(Game, related_name="players")
    pong_wins = models.IntegerField(default=0)
    pong_losses = models.IntegerField(default=0)
    pong_draws = models.IntegerField(default=0)
    pong_games_played = models.IntegerField(default=0)
    ttt_wins = models.IntegerField(default=0)
    ttt_losses = models.IntegerField(default=0)
    ttt_draws = models.IntegerField(default=0)
    ttt_games_played = models.IntegerField(default=0)
    tfa = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False, editable=True)
    is_playing = models.BooleanField(default=False, editable=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    idiom = models.CharField(max_length=10, choices=IDIOMS, default="EN")
    otp = models.CharField(default=None, max_length=64, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)
    intra42_id = models.BigIntegerField(unique=True, null=True)
    intra42_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save(update_fields=["last_seen"])
        # last_seen = cache.get('seen_%s' % self.username)
        # if last_seen:
        #     self.last_seen = last_seen
        #     self.save()
        # return last_seen

    def update_is_online(self):
        if self.last_seen:
            now = timezone.now()
            if now > self.last_seen + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                self.is_online = False
            else:
                self.is_online = True
        else:
            self.is_online = False
        self.save(update_fields=["is_online"])

    def get_is_online(self):
        self.update_is_online()
        return self.is_online
    
    # MAX_PONG_REQUESTS = 10

    # def add_pong_request(self, user):
    #     """
    #     Adds a pong request to the user, enforcing the maximum size.
    #     """
    #     if self.pong_requests.count() >= self.MAX_PONG_REQUESTS:
    #         raise ValueError(f"Cannot add more than {self.MAX_PONG_REQUESTS} pong requests.")
    #     self.pong_requests.add(user)

    # def add_ttt_request(self, user):
    #     """
    #     Adds a ttt request to the user, enforcing the maximum size.
    #     """
    #     if self.ttt_requests.count() >= self.MAX_PONG_REQUESTS:
    #         raise ValueError(f"Cannot add more than {self.MAX_PONG_REQUESTS} pong requests.")
    #     self.ttt_requests.add(user)