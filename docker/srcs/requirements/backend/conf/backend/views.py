from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
import requests
from urllib.parse import urlencode
# from requests_oauthlib import OAuth2Session

def oauth42_login(request):
    oauth_url = 'https://api.intra.42.fr/oauth/authorize'
    params = {
        'client_id': settings.OAUTH_42_CLIENT_ID,
        'redirect_uri': settings.OAUTH_42_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'public',
    }
    url = f"{oauth_url}?{urlencode(params)}"
    return redirect(url)

# def oauth42_login(request):
#     client_id = settings.OAUTH_42_CLIENT_ID
#     redirect_uri = settings.OAUTH_42_REDIRECT_URI
#     oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
#     authorization_url, state = oauth.authorization_url('https://api.intra.42.fr/oauth/authorize')
#     request.session['oauth_state'] = state
#     return redirect(authorization_url)

def oauth42_callback(request):
    code = request.GET.get('code')
    token_url = 'https://api.intra.42.fr/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': settings.OAUTH_42_CLIENT_ID,
        'client_secret': settings.OAUTH_42_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.OAUTH_42_REDIRECT_URI,
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    user_info_url = 'https://api.intra.42.fr/v2/me'
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = user_info_response.json()

    # Aqui você pode criar ou autenticar o usuário no seu sistema
    # Por exemplo:
    # user, created = User.objects.get_or_create(username=user_info['login'])
    # if created:
    #     user.email = user_info['email']
    #     user.save()
    # return redirect('/')
    return JsonResponse(user_info)

# def oauth42_callback(request):
#     client_id = settings.OAUTH_42_CLIENT_ID,
#     client_secret = settings.OAUTH_42_CLIENT_SECRET,
#     redirect_uri = settings.OAUTH_42_REDIRECT_URI,
#     oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, state=request.session['oauth_state'])
#     token = oauth.fetch_token('https://api.intra.42.fr/oauth/token', client_secret=client_secret, authorization_response=request.build_absolute_uri())
#     request.session['oauth_token'] = token
    
#     user_info_url = 'https://api.intra.42.fr/v2/me'
#     user_info_response = oauth.get(user_info_url)
#     user_info = user_info_response.json()

#     # Aqui você pode criar ou autenticar o usuário no seu sistema
#     # Por exemplo:
#     # user, created = User.objects.get_or_create(username=user_info['login'])
#     # if created:
#     #     user.email = user_info['email']
#     #     user.save()

#     return JsonResponse(user_info)
#     # return redirect('/')