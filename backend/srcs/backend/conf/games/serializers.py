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
            "owner_won",
            "draw",
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
            "owner_won",
            "draw",
            "winner",
            "game_type",
        )

    def validate(self, data):
        # Prevent updates if a winner is already set
        if self.instance and self.instance.owner_won is not None and self.instance.draw is not None and self.instance.result is not None:
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
            "owner_won",
            "draw",
            "winner",
            "game_type",
        )
    def validate(self, data):
        # logger.debug("Validating data: %s", data)
        # Check if all required fields are provided
        required_fields = ["player1",
            "player2",
            "result",
            "owner_won",
            "draw",
            "winner",
            "game_type"]
        for field in required_fields:
            if data.get(field) in [None, ""]:
                raise serializers.ValidationError(f"The field '{field}' cannot be empty.")

        # Check if either 'owner_won' or 'draw' is set to True
        owner_won = data.get("owner_won")
        draw = data.get("draw")
        if owner_won is None and draw is None:
            raise serializers.ValidationError("Either 'owner_won' or 'draw' must be set.")
        if owner_won == True and draw == True:
            raise serializers.ValidationError("Only one of 'owner_won' or 'draw' can be set to True.")

        return data