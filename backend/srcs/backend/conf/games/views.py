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
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IsGameOwner(BasePermission):
    """
    Custom permission to allow only the owner of the game to create or edit it.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user_pk in the URL matches the logged-in user's ID
        user_pk = view.kwargs.get("user_pk")
        return request.user.id == user_pk

class ListGamesView(generics.ListAPIView):
    serializer_class = ListGamesSerializer

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        return Game.objects.filter(user__id=user_pk)


class GameDetailsView(generics.RetrieveAPIView):
    serializer_class = ListGamesSerializer

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        game_pk = self.kwargs.get("game_pk")
        return Game.objects.filter(user__id=user_pk, game_id=game_pk)


class RetrieveUpdateGameView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateGameSerializer
    lookup_field = "game_id"
    lookup_url_kwarg = "game_pk"
    permission_classes = [IsGameOwner]

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        return Game.objects.filter(user__id=user_pk)

def add_game_to_user(user_id, game):
    from users.models import User
    try:
        user = User.objects.get(id=user_id)
        user.game_list.add(game)
        user.save()
        logger.info(f"Game {game.game_id} successfully added to user {user_id}'s game list.")
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist.")
        raise

class CreateGameView(generics.CreateAPIView):
    serializer_class = CreateGameSerializer
    permission_classes = [IsGameOwner]

    def perform_create(self, serializer):
        from users.models import User
        user_pk = self.kwargs.get("user_pk")
        user = User.objects.get(id=user_pk)
        game = serializer.save(user=user)
        add_game_to_user(user_pk, game) 

