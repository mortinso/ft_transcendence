from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests

auth_urlft = (
	"https://api.intra.42.fr/oauth/authorize?"
	"client_id=u-s4t2ud-6f95013ff80b03205f10c6858a27d612b0471205a3be99b15a164083c741aa4f&"
	"redirect_uri=https%3A%2F%2Fft-transcendence.com%2Foauth2%2Flogin%2Fredirect&"
	"response_type=code"
)

# Create your views here.
def home(request: HttpRequest) -> JsonResponse:
	return JsonResponse({"message": "oauth2"})

@login_required(login_url="/oauth2/login")
def get_authenticated_user(request: HttpRequest):
	return JsonResponse({"msg": "Authenticated"})

def ft_login(request: HttpRequest):
	return redirect(auth_urlft)

def ft_login_redirect(request: HttpRequest):
    code = request.GET.get("code")
    user_data = exchange_code(code)
    user = authenticate(request, user_data=user_data)
    if user is not None:
        login(request, user)
        return JsonResponse({"user": user_data})
    return JsonResponse({"error": "Authentication failed"}, status=401)

def exchange_code(code: str):
	data = {
		"client_id": "u-s4t2ud-6f95013ff80b03205f10c6858a27d612b0471205a3be99b15a164083c741aa4f",
		"client_secret": "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",
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": "https://ft-transcendence.com/oauth2/login/redirect",
		"scope": "public"
	}
	headers = {
		"Content-Type": "application/x-www-form-urlencoded",
	}
	response = requests.post("https://api.intra.42.fr/oauth/token", data=data, headers=headers)
	print(response)
	print(" <--response")
	credentials = response.json()
	access_token = credentials.get("access_token")
	response = requests.get("https://api.intra.42.fr/v2/me/", headers={
		"Authorization": "Bearer %s" % access_token
	})
	print(response)
	user = response.json()
	filtered_user = {
		"id": user.get("id"),
		"email": user.get("email"),
		"avatar": user.get("image", {}).get("link"),
		"login": user.get("login"),
		"first_name": user.get("first_name"),
		"last_name": user.get("last_name"),
		"url": user.get("url")
	}
	print(filtered_user)
	return filtered_user # user