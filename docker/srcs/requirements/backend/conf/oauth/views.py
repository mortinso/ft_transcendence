from django.shortcuts import redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from .exceptions import OauthAuthenticationError
import logging
import requests
from environs import Env
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from django.core.cache import cache
from django.contrib.auth import get_user_model



logger = logging.getLogger(__name__)

env = Env()

client_id = env("INTRA42_CLIENT_ID")
client_secret = env("INTRA42_CLIENT_SECRET")
auth_url = "https://api.intra.42.fr/oauth/authorize"
token_url = "https://api.intra.42.fr/oauth/token"
get_user_url = "https://api.intra.42.fr/v2/me/"
redirect_uri = "/api/oauth/login/redirect"

def login_42user(request: HttpRequest):
    host = request.get_host()
    return redirect(f"{auth_url}?client_id={client_id}&redirect_uri=https%3A%2F%2F{host}{redirect_uri}&response_type=code")


def login_redirect_42user(request: HttpRequest):
    code = request.GET.get("code")
    if not code:
        return redirect(f"/?error=Authorization code missing.")
    
    host = request.get_host()

    try:
        user_data = exchange_code_for_42user_info(code, host)
    except Exception as e:
        logger.error(f"Error getting user data: {e}")
        return redirect(f"/?error=Failed to get user data.")

    if not user_data or not user_data.get("id"):
        return redirect(f"/?error=Incomplete user data.")
    
    User42 = get_user_model()

    intra42_id = user_data.get("id")
    try:
        existent_user = User42.objects.get(intra42_id=intra42_id)
        if existent_user.is_active is False:
            return redirect(f"/?error=User is deactivated.")
    except User42.DoesNotExist:
        pass

    try:
        user = authenticate(request, user_data=user_data)
    except OauthAuthenticationError as auth_err:
        return redirect(f"/?error={auth_err.message}")

    if user:
        if cache.get(f"user_online_{user.id}"):
            return redirect(f"/?error=User already logged in.")
        
        login(request, user)
        cache.set(f"user_online_{user.id}", True, timeout=3600)
        user.is_online = True
        user.save()
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        redirect_url = f"/?access={str(refresh.access_token)}&refresh={str(refresh)}"
        return redirect(redirect_url)


def logout_42user(request: HttpRequest):
    logger.info(f"User {request.user} is logging out.")
    
    try:
        if request.user.is_authenticated:
            user = request.user
            user.is_online = False
            user.save()
            cache.delete(f"user_online_{user.id}")
    finally:
        logout(request)
        request.session.flush()
    
    response = redirect("/?logout=success")
    response.delete_cookie("sessionid")
    response.delete_cookie("csrftoken")
    
    return response


def exchange_code_for_42user_info(code: str, host: str):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"https://{host}{redirect_uri}",
        "scope": "public",
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=data, headers=headers)
    response.raise_for_status()

    credentials = response.json()
    access_token = credentials.get("access_token")
    if not access_token:
        logger.error(f"Access token not found in response: {credentials}")
        raise ValueError("Access token not found in response.")

    response = requests.get(
        get_user_url, headers={"Authorization": "Bearer %s" % access_token}
    )
    
    user = response.json()
    
    filtered_user = {
        "id": user.get("id"),
        "email": user.get("email"),
        "avatar": user.get("image", {}).get("link"),
        "login": user.get("login"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "url": user.get("url"),
    }

    return filtered_user