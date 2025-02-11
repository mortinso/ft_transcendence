from django.urls import path
from oauth2 import views

urlpatterns = [
    path("login/", views.login_42user, name="oauth-login"),
    path("logout/", views.logout_42user, name="oauth-logout"),
    path("login/redirect", views.login_redirect_42user, name="oauth-login-redirect"),
    path("user/", views.get_authenticated_user, name="get_authenticated_user"),
]
