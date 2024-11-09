# Instruções

1.  Define password in each /secrets file

2.  make

3.  Browser: http://127.0.0.1:8080

# Endpoints

http://127.0.0.1:8080/api/users (list users)

http://127.0.0.1:8080/api/users/1 (retrieve user 1, if user accessing is authenticated, else shows 404)

http://127.0.0.1:8080/api/users/1/edit (update, destroy user1, if user 1 is current user, else shows 404)

http://127.0.0.1:8080/api/auth/login (login)

http://127.0.0.1:8080/api/auth/logout (logout)