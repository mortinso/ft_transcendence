from django.urls import path, inlcude
from games.views import (
    ListGamesView,
    # GameDetailsView,
    RetrieveUpdateGameView,
)
from .views import (
    ListUsersView,
    UserDetailsView,
    WhoAmIView,
    RetrieveUpdateDestroyUserView,
    AddFriendView,
    RemoveFriendView,
    AcceptFriendView,
    RemoveFriendRequestView,
    BlockUserView,
    UnblockUserView,
    AddAvatarView,
    GetImageView,
    InvitePongView,
    AcceptPongView,
    InviteTTTView,
    AcceptTTTView,
)

urlpatterns = [
    path("whoami/", WhoAmIView.as_view(), name="whoami"),
    path("<uuid:pk>/edit/", RetrieveUpdateDestroyUserView.as_view(), name="user_update"),
    path("<uuid:pk>/invite_friend/", AddFriendView.as_view(), name="invite_friend"),
    path("<uuid:pk>/accept_friend/", AcceptFriendView.as_view(), name="accept_friend"),
    path("<uuid:pk>/remove_friend/", RemoveFriendView.as_view(), name="remove_friend"),
    path("<uuid:pk>/remove_friend_request/", RemoveFriendRequestView.as_view(), name="remove_friend_request"),
    path("<uuid:pk>/invite_to_pong/", InvitePongView.as_view(), name="invite_pong"),
    path("<uuid:pk>/accept_pong_invite/", AcceptPongView.as_view(), name="accept_pong"),
    path("<uuid:pk>/invite_to_ttt/", InviteTTTView.as_view(), name="invite_ttt"),
    path("<uuid:pk>/accept_ttt_invite/", AcceptTTTView.as_view(), name="accept_ttt"),
    path("<uuid:pk>/block/", BlockUserView.as_view(), name="block_user"),
    path("<uuid:pk>/unblock/", UnblockUserView.as_view(), name="unblock_user"),
    path("<uuid:pk>/add_avatar/", AddAvatarView.as_view(), name="add_avatar"),
    path("<uuid:pk>/get_avatar/", GetImageView.as_view(), name="get_avatar"),
    path("<uuid:pk>/", UserDetailsView.as_view(), name="user_details"),
    path("", ListUsersView.as_view(), name="user_list"),
    path("<uuid:pk>/games/edit/", RetrieveUpdateGameView.as_view(), name="game_update"),
]
