from django.urls import path
from .views import CreateUserView, ListUsersView, UserDetailsView, RetrieveUpdateDestroyUserView
from django.contrib.auth import views

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="user_create"),
    path("<pk>/", UserDetailsView.as_view(), name="user_list"),
    path("<pk>/edit", RetrieveUpdateDestroyUserView.as_view(), name="user_list"),
    path("", ListUsersView.as_view(), name="user_list"),
]