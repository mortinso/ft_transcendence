# Instruções

1.  Define password in each /secrets file

2.  to build and run the containers use: `make`

3.  Browser: <HOST_IP>

# Endpoints

## Users

### Listing and updating

/api/users (list users except current user)

/api/users/<uuid> (retrieve user <uuid>, if it exists)

/api/users/whoami (retrieves current user)

/api/users/1/edit (update/destroy user1, if user 1 is current user, else show 404) - 'username', 'email', 'old_password', 'password', 'confirm_password', 'first_name', 'last_name'

/api/users/1/add_avatar (add or update avatar) - 'avatar'

### Friends

/api/users/1/invite_friend (send friend request from user 1)

/api/users/1/accept_friend (accept friend requests)

/api/users/1/remove_friend (remove friend)

/api/users/1/remove_friend_request (remove friend request)

/api/users/1/block (block user)

/api/users/1/unblock (unblock user)

## Images

/api/users/<uuid:pk>/add_avatar/ (add user avatar)

/api/users/<uuid:pk>/get_avatar/ (get user avatar)

## Auth

/api/login/ (login)

/api/auth/logout/ (logout)

/api/auth/signup/ (signup)

/api/auth/check_otp/ (confirm user's one-time password)

### Signup instructions

On signup, a 6-digit one time password is sent to the user email. That password must be then sent to /api/auth/check_otp/ as 'otp'. If the OTP is valid, the page will return 200: OTP OK and the user is created.

### TFA instructions

If the user's tfa option is active, when the user logs in, a 6-digit one time password is sent to the user email. That password must be then sent to /api/auth/check_otp/ as 'otp'. If the OTP is valid, the page will return the JWT tokens.

## Oauth intra.42.fr

`/api/oauth/login` (oauth2 authentication)

`/api/oauth/logout` (oauth2 logout)

`/api/oauth/redirect` (oauth2 redirect)

`/api/oauth/user` (oauth2 check if user is logged in)