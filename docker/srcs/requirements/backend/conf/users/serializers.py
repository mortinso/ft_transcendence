from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User

class CreateUserSerializer(serializers.ModelSerializer):
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
    
class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'games_played', 'wins', 'losses', 'draws')

class UpdateUserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=100, write_only=True, required=False)
    confirm_password = serializers.CharField(max_length=100, write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'old_password', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'old_password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        if data.get('password') or data.get('confirm_password'):
            if not data.get('old_password'):
                raise serializers.ValidationError("Old password is required to set a new password.")
            if not self.instance.check_password(data.get('old_password')):
                raise serializers.ValidationError("Old password doesn't match.")
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def update(self, instance, validated_data):
        validated_data.pop('old_password', 'confirm_password')
        for attr, value in validated_data.items():
            if attr == 'password':
                self.validate_password(value)
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
            instance.save()
        return instance
    