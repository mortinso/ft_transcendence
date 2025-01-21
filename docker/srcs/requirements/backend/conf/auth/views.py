import random
import datetime
from django.utils import timezone
import hashlib
from .serializers import LoginSerializer, SignUpSerializer, CheckOTPSerializer, ForgotPasswordSerializer
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
import logging

logger = logging.getLogger(__name__)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user is not None and user.is_active:
            if user.tfa == True:
                otp = str(random.randint(000000, 999999))
                user.otp = hashlib.sha256(otp.encode()).hexdigest()
                user.otp_expiration = timezone.now() + datetime.timedelta(minutes=5)
                user.save()
                request.session['email'] = user.email  # Store email in session
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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        otp = str(random.randint(000000, 999999))
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()
        otp_expiration = timezone.now() + datetime.timedelta(minutes=5)
        request.session['otp_hash'] = otp_hash
        request.session['otp_expiration'] = otp_expiration.isoformat()
        request.session['user_data'] = user_data
        try:
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp}",
                settings.EMAIL_HOST_USER,
                [user_data['email']],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response({"error": "Unable to send email."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "An email was sent if the email is valid."}, status=status.HTTP_200_OK)


# class GetOTPView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = ForgotPasswordSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         try:
#             otp = str(random.randint(100000, 999999))
#             user = User.objects.get(email=email)
#             user.otp = hashlib.sha256(otp.encode()).hexdigest()
#             user.otp_expiration = timezone.now() + datetime.timedelta(minutes=5)
#             user.save()
#             try:
#                 send_mail(
#                     "Your OTP Code",
#                     f"Your OTP code is {otp}",
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 return Response({"error": "Failed to send email"}, status=status.HTTP_400_BAD_REQUEST)
#             return Response({"detail": "An email was sent if the email is valid."}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             pass
#         return Response({"detail": "An email was sent if the email is valid."}, status=status.HTTP_200_OK)


class CheckOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        purpose = serializer.validated_data['purpose']
        
        otp_hash = request.session.get('otp_hash')
        otp_expiration = request.session.get('otp_expiration')
        user_data = request.session.get('user_data') if purpose == 'signup' else None
        email = user_data['email'] if user_data else request.session.get('email')

        if not otp_hash or not otp_expiration or (purpose == 'signup' and not user_data):
            return Response({"detail": "OTP session data not found."}, status=status.HTTP_400_BAD_REQUEST)

        if purpose == 'signup':
                user_serializer = SignUpSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                if hashlib.sha256(otp.encode()).hexdigest() == otp_hash and timezone.now() < datetime.datetime.fromisoformat(otp_expiration):
                    user = user_serializer.save()
                    return Response({"detail": "OTP OK."}, status=status.HTTP_201_CREATED)
        elif purpose == 'tfa':
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
                
            logger.error(f"tfa: {user.otp}, {hashlib.sha256(otp.encode()).hexdigest()}, {purpose}")
            if hashlib.sha256(otp.encode()).hexdigest() == user.otp and user.otp_expiration > timezone.now():
                refresh = RefreshToken.for_user(user)
                update_last_login(None, user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)