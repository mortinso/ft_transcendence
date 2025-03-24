from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ListUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "date_joined",
            "is_online",
            "avatar",
            "last_seen",
            "friends",
            "friend_requests",
            "blocked",
            "wins",
            "losses",
            "draws",
            "games_played",
            "tfa",
            "idiom",
            "intra42_id",
        )
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request", None)
        if request and request.user != instance:
            fields_to_remove = ["email", "last_seen", "friend_requests", "blocked", "tfa"]
            for field in fields_to_remove:
                representation.pop(field, None)
        return representation


class UpdateUserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=126, write_only=True, required=False)
    confirm_password = serializers.CharField(max_length=126, write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "old_password",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "tfa",
            "idiom",
        )
        extra_kwargs = {
            "username": {"required": False},
            "password": {"write_only": True, "required": False},
            "email": {"required": False},
            "old_password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, data):
        if data.get('password') or data.get('confirm_password'):
            try:
                validate_password(data.get('password'))
                validate_password(data.get('confirm_password'))
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
            if not data.get('old_password'):
                raise serializers.ValidationError("Old password is required to set a new password.")
            if not self.instance.check_password(data.get('old_password')):
                raise serializers.ValidationError("Old password doesn't match.")
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data):
        validated_data.pop("old_password", "confirm_password")
        for attr, value in validated_data.items():
            if attr == "password":
                validate_password(self, value)
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
            instance.save()
        return instance


class AddAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "avatar")
        extra_kwargs = {
            "username": {"read_only": True},
            # 'avatar': {'write_only': True},
        }

    def save(self, *args, **kwargs):
        user = self.instance
        avatar = self.validated_data.get("avatar")
        if avatar:
            # Delete the existing file using default_storage
            if user.avatar and user.avatar.name != "default.jpg":
                if default_storage.exists(user.avatar.name):
                    default_storage.delete(user.avatar.name)
            user.avatar = avatar
            user.save()

            img_path = user.avatar.path
            img = Image.open(img_path)
            size = 300, 300
            img.thumbnail(size)
            img.save(img_path)

        return user


class AddFriendSerializer(serializers.ModelSerializer):
    add_friend = serializers.CharField(max_length=126, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "friends", "friend_requests", "add_friend")
        extra_kwargs = {
            "username": {"read_only": True},
            "friends": {"read_only": True},
            "friend_requests": {"read_only": True},
        }

    def update(self, instance, validated_data):
        friend = get_object_or_404(User, username=validated_data.get("add_friend"))

        if friend != instance:
            if friend not in instance.friends.all() and friend not in instance.friend_requests.all():
                friend.friend_requests.add(instance)
                friend.save()
        return instance


class AcceptFriendSerializer(serializers.ModelSerializer):
    accept_friend = serializers.CharField(max_length=126, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "friends", "friend_requests", "accept_friend")
        extra_kwargs = {
            "username": {"read_only": True},
            "friends": {"read_only": True},
            "friend_requests": {"read_only": True},
        }

    def update(self, instance, validated_data):
        friend = get_object_or_404(User, username=validated_data.get("accept_friend"))

        if friend != instance and friend in instance.friend_requests.all():
            instance.friends.add(friend)
            instance.friend_requests.remove(friend)
            friend.friends.add(instance)
            instance.save()
            friend.save()
        return instance


class RemoveFriendSerializer(serializers.ModelSerializer):
    remove_friend = serializers.CharField(max_length=126, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "friends", "remove_friend")
        extra_kwargs = {"username": {"read_only": True}, "friends": {"read_only": True}}

    def update(self, instance, validated_data):
        friend = get_object_or_404(User, username=validated_data.get("remove_friend"))

        if friend != instance and friend in instance.friends.all():
            instance.friends.remove(friend)
            friend.friends.remove(instance)
            instance.save()
        else:
            raise serializers.ValidationError("Friend not found.")
        return instance


class RemoveFriendRequestSerializer(serializers.ModelSerializer):
    remove_friend = serializers.CharField(max_length=126, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "friend_requests", "remove_friend")
        extra_kwargs = {"username": {"read_only": True}, "friend_requests": {"read_only": True}}

    def update(self, instance, validated_data):
        friend = get_object_or_404(User, username=validated_data.get("remove_friend"))

        if friend != instance and friend in instance.friend_requests.all():
            instance.friend_requests.remove(friend)
            instance.save()
        else:
            raise serializers.ValidationError("Friend request not found.")
        return instance


class BlockUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=126, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "blocked", "user")
        extra_kwargs = {"username": {"read_only": True}, "blocked": {"read_only": True}}

    def update(self, instance, validated_data):
        user = get_object_or_404(User, username=validated_data.get("user"))
        if user != instance:
            if user not in instance.blocked.all():
                instance.blocked.add(user)
                instance.save()
        else:
            raise serializers.ValidationError("User not found.")
        return instance


class UnblockUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=126, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "blocked", "user")
        extra_kwargs = {"username": {"read_only": True}, "blocked": {"read_only": True}}

    def update(self, instance, validated_data):
        user = get_object_or_404(User, username=validated_data.get("user"))
        if user != instance:
            if user in instance.blocked.all():
                instance.blocked.remove(user)
                user.save()
        else:
            raise serializers.ValidationError("User not found.")
        return instance
