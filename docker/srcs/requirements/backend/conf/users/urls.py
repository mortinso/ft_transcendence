from django.urls import path
from .views import ListUsersView, UserDetailsView, RetrieveUpdateDestroyUserView, WhoamiView, AddFriendView, RemoveFriendView, AcceptFriendView, RemoveFriendRequestView

urlpatterns = [
    path("<int:pk>/edit", RetrieveUpdateDestroyUserView.as_view(), name="user_update"),
    path("<int:pk>/add_friend", AddFriendView.as_view(), name="add_friend"),
    path("<int:pk>/accept_friend", AcceptFriendView.as_view(), name="accept_friend"),
    path("<int:pk>/remove_friend", RemoveFriendView.as_view(), name="remove_friend"),
    path("<int:pk>/remove_friend_request", RemoveFriendRequestView.as_view(), name="remove_friend_request"),
    path("<int:pk>/", UserDetailsView.as_view(), name="user_details"),
    path("whoami/", WhoamiView.as_view(), name="whoami"),
    path("", ListUsersView.as_view(), name="user_list"),
]