# Instruções

1.  Define password in each /secrets file

2.  make

3.  Browser: https://ft-transcendence.com

# Endpoints

## Users

### Listing and updating

https://ft-transcendence.com/api/users (list users except current user)

https://ft-transcendence.com/api/users/whoami (shows current user)

https://ft-transcendence.com/api/users/1 (retrieve user 1, if it exists)

https://ft-transcendence.com/api/users/1/edit (update/destroy user1, if user 1 is current user, else show 404)

### Friends

https://ft-transcendence.com/api/users/1/invite_friend (send friend request from user 1)

https://ft-transcendence.com/api/users/1/accept_friend (accept friend requests)

https://ft-transcendence.com/api/users/1/remove_friend (remove friend)

https://ft-transcendence.com/api/users/1/remove_friend_request (remove friend request)

https://ft-transcendence.com/api/users/1/block (block user)

https://ft-transcendence.com/api/users/1/unblock (unblock user)

## Auth

https://ft-transcendence.com/api/auth/login (login)

https://ft-transcendence.com/api/auth/logout (logout)

https://ft-transcendence.com/api/auth/signup (signup)