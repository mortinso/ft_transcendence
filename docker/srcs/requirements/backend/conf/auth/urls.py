from django.urls import path
from django.contrib.auth import views
from .views import LoginView, LogoutView, SignUpView
# from .views import document_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    # path('signup/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('media/<int:pk>/', document_view, name="document_view"),
]