from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .exceptions import OauthAuthenticationError
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class OauthAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user_data=None):
        if user_data is None:
            logger.error("user_data is None")
            raise OauthAuthenticationError("Incomplete user data.", status=400)

        logger.info(f"user_data: {user_data}")

        username = user_data.get("login")
        email = user_data.get("email")

        try:
            user = User.objects.get(username=username)
            if user.intra42_id:
                return user
            else:
                logger.error(f"User {username} has been created with a different method.")
                raise OauthAuthenticationError("A user with this username has already been created.", status=401)
        except User.DoesNotExist:
            if not username:
                logger.error("user_data does not contain 'username'")
                raise OauthAuthenticationError("Incomplete user data.", status=400)
            try:
                user = User.objects.get(email=email)
                if not user.intra42_id:
                    logger.error(f"User {email} has been created without 42 authentication.")
                    raise OauthAuthenticationError("A user with this email has already been created.", status=403)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    first_name=user_data.get("first_name"),
                    last_name=user_data.get("last_name"),
                    avatar=user_data.get("avatar"),
                    intra42_id=user_data.get("id"),
                    intra42_url=user_data.get("url"),
                )
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
