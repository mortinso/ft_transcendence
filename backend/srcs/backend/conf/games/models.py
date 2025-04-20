from django.db import models
from django.core.exceptions import ValidationError
import logging
import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

GAME_TYPES = (
    ("PONG", "pong"),
    ("TTT", "ttt"),
)

class Game(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="games", null=True, blank=True, editable=False)
    # active = models.BooleanField()
    player1 = models.CharField(max_length=10, default="Player1")
    player2 = models.CharField(max_length=10, default="Player2")
    result = models.CharField(max_length=3, default=None, null=True, blank=True)
    owner_won = models.BooleanField(default=None, null=True, blank=True)
    draw = models.BooleanField(default=None, null=True, blank=True)
    winner = models.CharField(max_length=10, default=None, null=True, blank=True)
    game_type = models.CharField(max_length=10, choices=GAME_TYPES, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.game_id)

    def create_user_stats(self):
        from users.models import User
        user = self.user
        
        if not user:
            return

        # Update stats based on the game type
        if self.game_type == "pong" or self.game_type == "PONG":
            user.pong_games_played += 1
            if self.owner_won:
                user.pong_wins += 1
            else:
                user.pong_losses += 1
        elif self.game_type == "ttt" or self.game_type == "TTT":
            user.ttt_games_played += 1
            if self.draw:
                user.ttt_draws += 1
            elif self.owner_won:
                user.ttt_wins += 1
            else:
                user.ttt_losses += 1
        # Save the updated stats
        user.save()