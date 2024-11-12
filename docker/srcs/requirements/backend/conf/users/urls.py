from django.urls import path
from .views import ListUsersView, UserDetailsView, RetrieveUpdateDestroyUserView, WhoamiView
from django.contrib.auth import views

urlpatterns = [
    path("<int:pk>/edit", RetrieveUpdateDestroyUserView.as_view(), name="user_update"),
    path("<int:pk>/", UserDetailsView.as_view(), name="user_details"),
    path("whoami/", WhoamiView.as_view(), name="whoami"),
    path("", ListUsersView.as_view(), name="user_list"),
]