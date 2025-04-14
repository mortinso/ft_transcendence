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


class UpdateGameSerializer(serializers.ModelSerializer):

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