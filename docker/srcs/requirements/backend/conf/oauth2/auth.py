from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

# check if user exists in the database (username, id, email, 42_id)
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
                email=user_data.get("email"),
                username=user_data.get("login"),
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
