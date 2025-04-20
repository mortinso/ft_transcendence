from django.db.models.signals import post_save
from django.dispatch import receiver
from games.models import Game
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@receiver(post_save, sender=Game)
def update_user_stats_on_create(sender, instance, created, **kwargs):
    """
    Update user stats when a new game is created.
    """
    if created:  # Only run when a new game is created
        logger.info(f"Game successfully added to user's game list.")
        instance.create_user_stats()