import random
import datetime
from django.utils import timezone
import hashlib
from .serializers import LoginSerializer, SignUpSerializer, ForgotPasswordSerializer, CheckOTPSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import update_last_login
from users.models import User
from django.core.mail import send_mail
from django.conf import settings

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user is not None:
            if user.tfa == True:
                otp = str(random.randint(100000, 999999))
                user.otp = hashlib.sha256(otp.encode()).hexdigest()
                user.otp_expiration = timezone.now() + datetime.timedelta(minutes=5)
                user.save()
                try:
                    send_mail(
                        "Your OTP Code",
                        f"Your OTP code is {otp}",
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    return Response({"error": "Failed to send email"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": "Email sent."}, status=status.HTTP_200_OK)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        user = request.user
        user.is_online = False
        user.save()
        logout(request)
        request.session.flush()
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')
        return response
    
class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

class GetOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            otp = str(random.randint(100000, 999999))
            user = User.objects.get(email=email)
            user.otp = hashlib.sha256(otp.encode()).hexdigest()
            user.otp_expiration = timezone.now() + datetime.timedelta(minutes=5)
            user.save()
            try:
                send_mail(
                    "Your OTP Code",
                    f"Your OTP code is {otp}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({"error": "Failed to send email"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "An email was sent if the email is valid."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass
        return Response({"detail": "An email was sent if the email is valid."}, status=status.HTTP_200_OK)
    

class CheckOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        user = User.objects.get(email=email)
        if user is not None:
            login(request, user)
            if user.otp == hashlib.sha256(otp.encode()).hexdigest() and user.otp_expiration > timezone.now():
                refresh = RefreshToken.for_user(user)
                update_last_login(None, user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Invalid email."}, status=status.HTTP_400_BAD_REQUEST)