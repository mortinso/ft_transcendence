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
        
class GenerateMediaAccessToken(APIView):
    permission_classes = [IsSelf]

    def get(self, request, pk):
        if self.request.user.id != pk:
            return Response({"404 Not Found"}, status=status.HTTP_404_NOT_FOUND)
        file_name = self.request.user.avatar
        route = '/media/' + str(self.request.user.avatar)
        response = HttpResponse()
        response["X-Accel-Redirect"] = route
        # response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        # del response['Content-Type']
        # del response['Accept-Ranges']
        # del response['Set-Cookie']
        # del response['Cache-Control']
        # del response['Expires']
        return response
        
class GetImage(APIView):
    prefix = ""
    def get(self, request):
        hashed_code = request.query_params.get('hashed_code')
        log_type = request.query_params.get('log_type', 'Lightning')
        file_name = request.query_params.get('file_name', '')
        route = '/download-logs/' + file_name if log_type == 'Lightning' else '/download-logs/' + file_name
        response = HttpResponse()
        response["X-Accel-Redirect"] = route
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        del response['Content-Type']
        del response['Accept-Ranges']
        del response['Set-Cookie']
        del response['Cache-Control']
        del response['Expires']
        return response