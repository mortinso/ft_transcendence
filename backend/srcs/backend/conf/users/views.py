from django.shortcuts import render, redirect
from .models import User
from .serializers import (
    ListUsersSerializer,
    UpdateUserSerializer,
    AddFriendSerializer,
    RemoveFriendSerializer,
    AcceptFriendSerializer,
    RemoveFriendRequestSerializer,
    BlockUserSerializer,
    UnblockUserSerializer,
    AddAvatarSerializer,
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


class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all().filter(is_active=True)

    serializer_class = ListUsersSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer


class WhoAmIView(generics.RetrieveAPIView):
    serializer_class = ListUsersSerializer

    def get_object(self):
        return generics.get_object_or_404(User, id=self.request.user.id)


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()

    def destroy(self, request, pk):
        user = generics.get_object_or_404(User, id=pk)
        if request.user.id != user.id:
            raise PermissionDenied("You cannot deactivate another user's account.")
        
        user.is_online = False
        user.is_active = False
        user.save()
        
        cache.delete(f"user_online_{user.id}")

        logout(request)
        request.session.flush()

        response = Response({"detail": "user deleted."}, status=status.HTTP_200_OK)
        response.delete_cookie("sessionid")
        response.delete_cookie("csrftoken")

        return response

    serializer_class = UpdateUserSerializer


class AddAvatarView(generics.UpdateAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = AddAvatarSerializer


class AddFriendView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = AddFriendSerializer


class AcceptFriendView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = AcceptFriendSerializer


class RemoveFriendView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = RemoveFriendSerializer


class RemoveFriendRequestView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = RemoveFriendRequestSerializer


class BlockUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = BlockUserSerializer


class UnblockUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = UnblockUserSerializer


class GetImageView(APIView):
    def get(self, request, pk):
        user = generics.get_object_or_404(User, id=pk)
        logger.debug(f"user.avatar: {user.avatar}")
        avatar_url = str(user.avatar)
        
        if avatar_url.startswith('http://') or avatar_url.startswith('https://'):
            try:
                logger.debug(f"Proxying the external image: {avatar_url}")
                img_response = requests.get(avatar_url)
                img_response.raise_for_status()
                
                response = HttpResponse(
                    content=img_response.content,
                    content_type=img_response.headers.get('Content-Type', 'image/jpeg')
                )
                return response
            except Exception as e:
                logger.error(f"Erro ao buscar avatar externo: {e}")
                return HttpResponse(status=404)
        
        route = "/media/" + avatar_url
        logger.debug(f"Servindo arquivo local: {route}")
        response = HttpResponse()
        response["X-Accel-Redirect"] = route
        return response