from django.shortcuts import redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .exceptions import OauthAuthenticationError
import logging
import requests
from environs import Env
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from django.core.cache import cache


logger = logging.getLogger(__name__)

env = Env()

auth_url = env("INTRA42_AUTH_URL")
client_id = env("INTRA42_CLIENT_ID")
client_secret = env("INTRA42_CLIENT_SECRET")
redirect_uri = env("INTRA42_REDIRECT_URI")
token_url = "https://api.intra.42.fr/oauth/token"
get_user_url = "https://api.intra.42.fr/v2/me/"


def login_42user(request: HttpRequest):
    return redirect(auth_url)


def login_redirect_42user(request: HttpRequest):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code missing."}, status=400)

    try:
        user_data = exchange_code_for_42user_info(code)
    except Exception as e:
        logger.error(f"Error getting user data: {e}")
        return JsonResponse({"error": "Failed to get user data."}, status=500)

    if not user_data or not user_data.get("id"):
        return JsonResponse({"error": "Incomplete user data."}, status=400)

    try:
        user = authenticate(request, user_data=user_data)
    except OauthAuthenticationError as auth_err:
        return JsonResponse({"error": auth_err.message}, status=auth_err.status)

    if user:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        redirect_url = f"/?access={str(refresh.access_token)}&refresh={str(refresh)}"
        return redirect(redirect_url)
    #     return JsonResponse(
    #         {
    #             "refresh": str(refresh),
    #             "access": str(refresh.access_token),
    #         },
    #         status=200,
    #     )
    # return JsonResponse({"error": "Authentication failed"}, status=401)


def logout_42user(request: HttpRequest):
    logger.info(f"User {request.user} is logging out.")
    user = request.user
    user.is_online = False
    user.save()
    logout(request)
    request.session.flush()
    response = JsonResponse({"detail": "Successfully logged out."}, status=200)
    response.delete_cookie("sessionid")
    return response


def exchange_code_for_42user_info(code: str):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": "public",
    }
    # headers = {"Content-Type": "application/x-www-form-urlencoded", "Access-Control-Allow-Origin": "*"}
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # headers = {"Content-Type": "application/json; charset=utf-8"}
    # response = requests.post(token_url, data=data, headers=headers)
    response = requests.post(token_url, data=data)
    credentials = response.json()
    access_token = credentials.get("access_token")
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
