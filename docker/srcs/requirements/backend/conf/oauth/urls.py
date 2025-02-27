from django.urls import path
from oauth import views

urlpatterns = [
    path("login/", views.login_42user, name="oauth-login"),
    path("logout/", views.logout_42user, name="oauth-logout"),
    path("login/redirect", views.login_redirect_42user, name="oauth-login-redirect"),
]
