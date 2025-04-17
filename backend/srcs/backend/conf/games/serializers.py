from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Game
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ListGamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = (
            "game_id",
            "date",
            "user",
            "player1",
            "player2",
            "result",
            "winner",
            "game_type",
        )


class RetrieveUpdateGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = (
            "game_id",
            "date",
            "user",
            "player1",
            "player2",
            "result",
            "winner",
            "game_type",
        )

    def validate(self, data):
        # Prevent updates if a winner is already set
        if self.instance and self.instance.winner is not None and self.instance.result is not None:
            raise serializers.ValidationError("This game is locked because a winner and result have already been set.")
        return data


class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            "game_id",
            "date",
            "user",
            "player1",
            "player2",
            "result",
            "winner",
            "game_type",
        )