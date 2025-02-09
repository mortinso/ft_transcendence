from django.contrib.auth.backends import BaseBackend
from .models import Intra42Profile
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class Oauth2AuthenticationBackend(BaseBackend):
    def authenticate(self, request, user_data=None):
        if user_data is None:
            logger.error("user_data is None")
            return None

        logger.info(f"user_data: {user_data}")

        try:
            user = User.objects.get(username=user_data.get("login"))
        except User.DoesNotExist:
            if not user_data.get("login"):
                logger.error("user_data does not contain 'login'")
                return None

            user = User.objects.create_user(
                username=user_data.get("login"),
                email=user_data.get("email"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
            )
            Intra42Profile.objects.create(
                user=user,
                intra42_id=user_data.get("id"),
                email=user_data.get("email"),
                avatar=user_data.get("avatar"),
                login=user_data.get("login"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                url=user_data.get("url"),
            )
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
