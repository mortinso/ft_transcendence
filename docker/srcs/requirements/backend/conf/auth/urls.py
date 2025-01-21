from django.urls import path
from django.contrib.auth import views
from .views import LoginView, LogoutView, SignUpView, CheckOTPView
# from .views import document_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('get_otp/', GetOTPView.as_view(), name='check_otp'),
    path('check_otp/', CheckOTPView.as_view(), name='check_otp'),
    # path('media/<int:pk>/', document_view, name="document_view"),
]