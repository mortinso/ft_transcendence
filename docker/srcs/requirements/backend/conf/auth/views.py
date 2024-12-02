from django.shortcuts import render
from users.models import User
from .serializers import LoginSerializer, SignUpSerializer
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication 
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import update_last_login
from django.http import FileResponse, Http404
from django.conf import settings
import os



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        request.session.flush()
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')

        return response
    
class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

# def document_view(request, path):
#     # Check if the user is authenticated
#     if not request.user.is_authenticated:
#         raise Http404

#     # Construct the full file path
#     file_path = os.path.join(settings.MEDIA_ROOT, path)

#     # Check if the file exists
#     if not os.path.exists(file_path):
#         raise Http404

#     # Serve the file
#     return FileResponse(open(file_path, 'rb'))

