from django.urls import path
from .views import ListUsersView, UserDetailsView, WhoAmIView, RetrieveUpdateUserView, DestroyUserView, AddFriendView, RemoveFriendView, AcceptFriendView, RemoveFriendRequestView, BlockUserView, UnblockUserView, AddAvatarView, GetImageView

urlpatterns = [
    path("whoami/", WhoAmIView.as_view(), name="whoami"),
    path("<uuid:pk>/edit/", RetrieveUpdateUserView.as_view(), name="user_update"),
    path("<uuid:pk>/delete/", DestroyUserView.as_view(), name="user_update"),
    path("<uuid:pk>/invite_friend/", AddFriendView.as_view(), name="invite_friend"),
    path("<uuid:pk>/accept_friend/", AcceptFriendView.as_view(), name="accept_friend"),
    path("<uuid:pk>/remove_friend/", RemoveFriendView.as_view(), name="remove_friend"),
    path("<uuid:pk>/remove_friend_request/", RemoveFriendRequestView.as_view(), name="remove_friend_request"),
    path("<uuid:pk>/block/", BlockUserView.as_view(), name="block_user"),
    path("<uuid:pk>/unblock/", UnblockUserView.as_view(), name="unblock_user"),
    path("<uuid:pk>/add_avatar/", AddAvatarView.as_view(), name="add_avatar"),
    path("<uuid:pk>/get_avatar/", GetImageView.as_view(), name="get_avatar"),
    path("<uuid:pk>/", UserDetailsView.as_view(), name="user_details"),
    path("", ListUsersView.as_view(), name="user_list"),
]