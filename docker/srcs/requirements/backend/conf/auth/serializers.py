from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import User
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)


class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_password")
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, data):
        if "email" not in data or not data["email"]:
            raise serializers.ValidationError("Email is required.")
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        try:
            user_check = User.objects.get(username=username)
            
            if not user_check.is_active:
                if user_check.check_password(password):
                    logger.warning(f"Login attempt with correct credentials for inactive user: {username}")
                    data["user"] = user_check
                    return data
                else:
                    raise serializers.ValidationError("Unable to log in with provided credentials.")
        except User.DoesNotExist:
            pass
        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        
        data["user"] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)


class CheckOTPSerializer(serializers.Serializer):
    # email = serializers.EmailField()
    otp = serializers.CharField()
    # purpose = serializers.CharField(required=True)
