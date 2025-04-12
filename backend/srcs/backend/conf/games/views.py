from django.shortcuts import render, redirect
from .models import Game
from .serializers import (
    ListGamesSerializer,
    UpdateGameSerializer,
)
from rest_framework import generics
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
    try:
        queryset = Game.objects.all()
    except:
        queryset = None

    serializer_class = ListGamesSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["request"] = self.request
    #     return context


class GameDetailsView(generics.RetrieveAPIView):
    try:
        queryset = Game.objects.all()
    except:
        queryset = None
    serializer_class = ListGamesSerializer


class RetrieveUpdateGameView(generics.RetrieveUpdateAPIView):
    try:
        queryset = Game.objects.all()
    except:
        queryset = None
    serializer_class = UpdateGameSerializer
