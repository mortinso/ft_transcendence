from django.shortcuts import render
from .models import User
from .serializers import ListUsersSerializer, UpdateUserSerializer, AddFriendSerializer, RemoveFriendSerializer, AcceptFriendSerializer, RemoveFriendRequestSerializer, BlockUserSerializer, UnblockUserSerializer
from rest_framework import generics

class ListUsersView(generics.ListAPIView):
    serializer_class = ListUsersSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all()
        queryset = queryset.exclude(id=user.id)
        return queryset


class UserDetailsView(generics.RetrieveAPIView):

    serializer_class = ListUsersSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return generics.get_object_or_404(User, pk=pk)
    
class WhoamiView(generics.RetrieveAPIView):

    serializer_class = ListUsersSerializer

    def get_object(self):
        return generics.get_object_or_404(User, id=self.request.user.id)

class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateUserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == self.request.user.id:
            return User.objects.filter(pk=pk)

class AddFriendView(generics.RetrieveUpdateAPIView):
    serializer_class = AddFriendSerializer
    # serializer_class = UpdateUserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == self.request.user.id:
            return User.objects.filter(pk=pk)
    
    
class AcceptFriendView(generics.RetrieveUpdateAPIView):
    serializer_class = AcceptFriendSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == self.request.user.id:
            return User.objects.filter(pk=pk)

class RemoveFriendView(generics.RetrieveUpdateAPIView):
    serializer_class = RemoveFriendSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == self.request.user.id:
            return User.objects.filter(pk=pk)

class RemoveFriendRequestView(generics.RetrieveUpdateAPIView):
    serializer_class = RemoveFriendRequestSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == self.request.user.id:
            return User.objects.filter(pk=pk)

class BlockUserView(generics.RetrieveUpdateAPIView):
    serializer_class = BlockUserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == self.request.user.id:
            return User.objects.filter(pk=pk)

class UnblockUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UnblockUserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == self.request.user.id:
            return User.objects.filter(pk=pk)
        
class returnImageView(generics.RetrieveUpdateAPIView):
    pass