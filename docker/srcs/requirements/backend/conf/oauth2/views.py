from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import logging
import requests


logger = logging.getLogger(__name__)

auth_urlft = (
	"https://api.intra.42.fr/oauth/authorize?"
    "client_id=u-s4t2ud-6f95013ff80b03205f10c6858a27d612b0471205a3be99b15a164083c741aa4f&"
    "redirect_uri=https%3A%2F%2Fft-transcendence.com%2Fapi%2Foauth%2Flogin%2Fredirect&"
    "response_type=code"
)

@login_required(login_url="/api/oauth/login")
def get_authenticated_user(request: HttpRequest):
	return JsonResponse({"msg": "Authenticated"})

def login_42user(request: HttpRequest):
	return redirect(auth_urlft)

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

    user = authenticate(request, user_data=user_data)
    if user is not None:
        login(request, user)
        return JsonResponse({"user": user_data})
    
    return JsonResponse({"error": "Authentication failed"}, status=401)

def logout_42user(request: HttpRequest):
    # Loga a ação (opcional)
    logger.info(f"User {request.user} is logging out.")
    
    logout(request)
    request.session.flush()  # Confirma que a sessão foi completamente limpa
    return JsonResponse({"detail": "Successfully logged out."}, status=200)

def exchange_code_for_42user_info(code: str):
	data = {
		"client_id": "u-s4t2ud-6f95013ff80b03205f10c6858a27d612b0471205a3be99b15a164083c741aa4f",
		"client_secret": "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",
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": "https://ft-transcendence.com/api/oauth/login/redirect",
		"scope": "public"
	}
	headers = { "Content-Type": "application/x-www-form-urlencoded" }
	response = requests.post("https://api.intra.42.fr/oauth/token", data=data, headers=headers)
	credentials = response.json()
	print(f'RESPONSE: {response}')
	print(f'CREDENDITALS: {credentials}')
	access_token = credentials.get("access_token")
	response = requests.get("https://api.intra.42.fr/v2/me/", headers={
		"Authorization": "Bearer %s" % access_token
	})
	print(f'RESPONSE: {response}')
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