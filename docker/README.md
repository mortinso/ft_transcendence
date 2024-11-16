# Instruções

1.  Define password in each /secrets file

2.  make

3.  Browser: http://127.0.0.1:8080

# Endpoints

## Users

### Listing and updating

http://127.0.0.1:8080/api/users (list users except current user)

http://127.0.0.1:8080/api/users/whoami (shows current user)

http://127.0.0.1:8080/api/users/1 (retrieve user 1, if it exists)

http://127.0.0.1:8080/api/users/1/edit (update/destroy user1, if user 1 is current user, else shows 404)

### Friends

http://127.0.0.1:8080/api/users/1/invite_friend (send friend request from user 1)

http://127.0.0.1:8080/api/users/1/accept_friend (accept friend requests)

http://127.0.0.1:8080/api/users/1/remove_friend (remove friend)

http://127.0.0.1:8080/api/users/1/remove_friend_request (remove friend request)

http://127.0.0.1:8080/api/users/1/block (block user)

http://127.0.0.1:8080/api/users/1/unblock (unblock user)

## Auth

http://127.0.0.1:8080/api/auth/login (login)

http://127.0.0.1:8080/api/auth/logout (logout)

http://127.0.0.1:8080/api/auth/signup (logout)