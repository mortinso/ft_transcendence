from django.shortcuts import render
from .models import User
from .serializers import ListUsersSerializer, UpdateUserSerializer, AddFriendSerializer, RemoveFriendSerializer, AcceptFriendSerializer, RemoveFriendRequestSerializer, BlockUserSerializer, UnblockUserSerializer, AddAvatarSerializer
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
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
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
    serializer_class = UpdateUserSerializer

class AddAvatarView(generics.UpdateAPIView):
    # permission_classes = [IsSelf]

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
        route = '/media/' + str(user.avatar)
        logger.debug(f"route: {route}")
        response = HttpResponse()
        response["X-Accel-Redirect"] = route
        del response['Content-Type']
        return response
        