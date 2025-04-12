from django.shortcuts import render, redirect
from .models import Game
from .serializers import (
    ListGamesSerializer,
    UpdateGameSerializer,
    CreateGameSerializer,
)
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from django.http import FileResponse
import os
from rest_framework.response import Response
from rest_framework import status
from backend.permissions import IsSelf
import hashlib
from django.http import HttpResponse
from rest_framework.exceptions import PermissionDenied
import logging
import requests
from django.core.cache import cache
from django.contrib.auth import logout


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ListGamesView(generics.ListAPIView):
    serializer_class = ListGamesSerializer

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        return Game.objects.filter(user__id=user_pk)

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["request"] = self.request
    #     return context


class GameDetailsView(generics.RetrieveAPIView):
    serializer_class = ListGamesSerializer

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        game_pk = self.kwargs.get("game_pk")
        return Game.objects.filter(user__id=user_pk, game_id=game_pk)


class RetrieveUpdateGameView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateGameSerializer
    lookup_field = "game_id"  # Match the field in the Game model
    lookup_url_kwarg = "game_pk"  # Match the URL keyword argument

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")  # Get the user UUID from the URL
        return Game.objects.filter(user__id=user_pk)  # Filter games by the user

def add_game_to_user(user_id, game_id):
    from users.models import User  # Ensure the User model is imported

def add_game_to_user(user_id, game):
    from users.models import User
    try:
        # Fetch the user instance
        user = User.objects.get(id=user_id)

        # Add the game to the user's game_list
        user.game_list.add(game)

        # Save the user instance (not strictly necessary for ManyToManyField)
        user.save()

        logger.info(f"Game {game.game_id} successfully added to user {user_id}'s game list.")
    except User.DoesNotExist:  # Reference the User model, not the local variable
        logger.error(f"User with ID {user_id} does not exist.")
        raise

class CreateGameView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateGameSerializer

    def perform_create(self, serializer):
        user_pk = self.kwargs.get("user_pk")  # Get the user UUID from the URL
        game = serializer.save()  # Save the game instance and get the created game object
        add_game_to_user(user_pk, game)  # Pass the game instance to the function

