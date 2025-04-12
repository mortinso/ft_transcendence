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
            "id",
            "date",
            "user",
            "player1",
            "player2",
            "result",
            "winner",
            "game_type",
        )

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     request = self.context.get("request", None)
    #     if request and request.user != instance:
    #         fields_to_remove = ["email", "last_seen", "friend_requests", "blocked", "tfa"]
    #         for field in fields_to_remove:
    #             representation.pop(field, None)
    #     return representation


class UpdateGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = (
            "player1",
            "player2",
            "result",
            "winner",
            "game_type",
        )

    # def validate(self, data):
    #     if data.get('password') or data.get('confirm_password'):
    #         try:
    #             validate_password(data.get('password'))
    #             validate_password(data.get('confirm_password'))
    #         except ValidationError as e:
    #             raise serializers.ValidationError(e.messages)
    #         if not data.get('old_password'):
    #             raise serializers.ValidationError("Old password is required to set a new password.")
    #         if not self.instance.check_password(data.get('old_password')):
    #             raise serializers.ValidationError("Old password doesn't match.")
    #         if data.get('password') != data.get('confirm_password'):
    #             raise serializers.ValidationError("Passwords do not match.")
    #     return data

    # def update(self, instance, validated_data):
    #     validated_data.pop("old_password", "confirm_password")
    #     for attr, value in validated_data.items():
    #         if attr == "password":
    #             validate_password(self, value)
    #             instance.set_password(value)
    #         else:
    #             setattr(instance, attr, value)
    #         instance.save()
    #     return instance
