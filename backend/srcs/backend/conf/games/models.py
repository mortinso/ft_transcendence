from django.db import models

import uuid

# TODO:on_delete

GAME_TYPES = (
    ("PONG", "pong"),
    ("TTT", "ttt"),
    ("pong", "pong"),
    ("ttt", "ttt"),
    ("None", "None"),
    (None, "None"), 
)

class Game(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="games", null=True, blank=True, editable=False)
    # active = models.BooleanField()
    player1 = models.CharField(max_length=10, default="Player1")
    player2 = models.CharField(max_length=10, default="Player2")
    result = models.CharField(max_length=3, default=None, null=True, blank=True)
    winner = models.CharField(max_length=10, default=None, null=True, blank=True)
    game_type = models.CharField(max_length=10, choices=GAME_TYPES, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.game_id)