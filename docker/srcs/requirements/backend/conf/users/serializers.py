from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User

class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'friends', 'friend_requests', 'blocked', 'games_played', 'wins', 'losses', 'draws')

class UpdateUserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=100, write_only=True, required=False)
    confirm_password = serializers.CharField(max_length=100, write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'old_password', 'password', 'confirm_password', 'first_name', 'last_name', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'old_password': {'write_only': True},
            'confirm_password': {'write_only': True},
            'avatar': {'write_only': True}
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
    
class AddFriendSerializer(serializers.ModelSerializer):
    add_friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'friends', 'friend_requests', 'add_friend')
        extra_kwargs = {'username': {'read_only': True}, 'friends': {'read_only': True}, 'friend_requests': {'read_only': True}}

    def update(self, instance, validated_data):
        friend = validated_data.get('add_friend')
        if friend != instance:
            if friend not in instance.friends.all() and friend not in instance.friend_requests.all():
                friend.friend_requests.add(instance)
                friend.save()
        else:
            raise serializers.ValidationError("User not found.")
        return instance
    
class AcceptFriendSerializer(serializers.ModelSerializer):
    accept_friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'friends', 'friend_requests', 'accept_friend')
        extra_kwargs = {'username': {'read_only': True}, 'friends': {'read_only': True}, 'friend_requests': {'read_only': True}}

    def update(self, instance, validated_data):
        friend = validated_data.get('accept_friend')

        if friend != instance and friend in instance.friend_requests.all():
            instance.friends.add(friend)
            instance.friend_requests.remove(friend)
            friend.friends.add(instance)
            instance.save()
            friend.save()
        else:
            raise serializers.ValidationError("Friend request not found.")
        return instance

class RemoveFriendSerializer(serializers.ModelSerializer):
    remove_friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'friends', 'remove_friend')
        extra_kwargs = {'username': {'read_only': True}, 'friends': {'read_only': True}}

    def update(self, instance, validated_data):
        friend = validated_data.get('remove_friend')

        if friend != instance and friend in instance.friends.all():
            instance.friends.remove(friend)
            friend.friends.remove(instance)
            instance.save()
        else:
            raise serializers.ValidationError("Friend not found.")
        return instance
    

class RemoveFriendRequestSerializer(serializers.ModelSerializer):
    remove_friend = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'friend_requests', 'remove_friend')
        extra_kwargs = {'username': {'read_only': True}, 'friend_requests': {'read_only': True}}

    def update(self, instance, validated_data):
        friend = validated_data.get('remove_friend')

        if friend != instance and friend in instance.friend_requests.all():
            instance.friend_requests.remove(friend)
            instance.save()
        else:
            raise serializers.ValidationError("Friend request not found.")
        return instance

class BlockUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'blocked', 'user')
        extra_kwargs = {'username': {'read_only': True}, 'blocked': {'read_only': True}}

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        if user != instance:
            if user not in instance.blocked.all():
                instance.blocked.add(user)
                instance.save()
        else:
            raise serializers.ValidationError("User not found.")
        return instance
    
class UnblockUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'blocked', 'user')
        extra_kwargs = {'username': {'read_only': True}, 'blocked': {'read_only': True}}

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        if user != instance:
            if user in instance.blocked.all():
                instance.blocked.remove(user)
                user.save()
        else:
            raise serializers.ValidationError("User not found.")
        return instance