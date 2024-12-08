from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import User
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}, 'email': {'required': True}}

    def validate(self, data):
        if 'email' not in data or not data['email']:
            raise serializers.ValidationError("Email is required.")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    # TFA = serializers.CharField(max_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data['user'] = user
        return data
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

class CheckOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()