from django.db import models
from users.models import User

# TODO:on_delete

GAME_TYPES = (
    ("PONG", "pong"),
    ("TTT", "ttt"),
    ("pong", "pong"),
    ("ttt", "ttt"),
    ("None", "None"),
    (None, "None"), 
)

class Game():
    game_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    # active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    player1 = models.CharField(max_length=10, default="Player1")
    player2 = models.CharField(max_length=10, default="Player2")
    result = models.CharField(max_length=3, default=None, null=True, blank=True)
    winner = models.CharField(max_length=10, default=None, null=True, blank=True)
    game_type = models.CharField(max_length=10, choices=GAME_TYPES, default=None, null=True, blank=True)

    def __str__(self):
        return self.id