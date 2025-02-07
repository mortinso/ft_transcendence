from django.contrib.auth.backends import BaseBackend
from .models import intra42User

class Oauth2AuthenticationBackend(BaseBackend):
	def authenticate(self, request, user) -> intra42User:
		find_user = intra42User.objects.filter(id=user.get("id"))
		if len(find_user) == 0:
			print("User was not found, Saving...")