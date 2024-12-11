from django.shortcuts import render
from .models import User
from .serializers import ListUsersSerializer, UpdateUserSerializer, AddFriendSerializer, RemoveFriendSerializer, AcceptFriendSerializer, RemoveFriendRequestSerializer, BlockUserSerializer, UnblockUserSerializer
from rest_framework import generics
from django.conf import settings
from django.http import FileResponse
import os
from rest_framework.response import Response
from rest_framework import status
from backend.permissions import IsSelf

class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = User.objects.all()
    #     queryset = queryset.exclude(id=user.id)
    #     return queryset

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer

class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSelf]

    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer

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
        
def returnImage(request, path):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Check if the file exists
    if not os.path.exists(file_path):
        return Response({"detail": "Invalid path"}, status=status.HTTP_400_BAD_REQUEST)

    # Serve the file
    return FileResponse(open(file_path, 'rb'))