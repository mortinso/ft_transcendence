from django.shortcuts import render
from .models import User
from .serializers import CreateUserSerializer, ListUsersSerializer, UpdateUserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib import messages


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

class ListUsersView(generics.ListAPIView):
    serializer_class = ListUsersSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

class UserDetailsView(generics.RetrieveAPIView):

    serializer_class = ListUsersSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return generics.get_object_or_404(User, pk=pk)

class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return User.objects.filter(id = self.request.user.id)
    serializer_class = UpdateUserSerializer
