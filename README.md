# Instruções

1.  Define passwords in a .env file

2.  to build and run the containers use: `make`

3.  Browser: <HOST_IP>

# Endpoints

## Users

### Listing and updating
- `/api/users` (list users except current user)

- `/api/users/<uuid>` (retrieve user <uuid>, if it exists)

- `/api/users/whoami` (retrieves current user)

- `/api/users/1/edit` (update/destroy user1, if user 1 is current user, else show 404) - 'username', 'email', 'old_password', 'password', 'confirm_password', 'first_name', 'last_name'

- `/api/users/1/add_avatar` (add or update avatar) - 'avatar'

### Friends
- `/api/users/1/invite_friend` (send friend request from user 1)

- `/api/users/1/accept_friend` (accept friend requests)

- `/api/users/1/remove_friend` (remove friend)

- `/api/users/1/remove_friend_request` (remove friend request)

- `/api/users/1/block` (block user)

- `/api/users/1/unblock` (unblock user)

### Images
- `/api/users/<uuid:pk>/add_avatar/` (add user avatar)

- `/api/users/<uuid:pk>/get_avatar/` (get user avatar)

### Auth
- `/api/login/` (login)

- `/api/auth/logout/` (logout)

- `/api/auth/signup/` (signup)

- `/api/auth/check_otp/` (confirm user's one-time password)

### Oauth
- `/api/oauth/login` (oauth2 authentication)
- `/api/oauth/logout` (oauth2 logout)

### Signup instructions

On signup, a 6-digit one time password is sent to the user email. That password must be then sent to /api/auth/check_otp/ as 'otp'. If the OTP is valid, the page will return 200: OTP OK and the user is created.

### TFA instructions

If the user's tfa option is active, when the user logs in, a 6-digit one time password is sent to the user email. That password must be then sent to /api/auth/check_otp/ as 'otp'. If the OTP is valid, the page will return the JWT tokens.

# ELK

## Import dashboard to Kibana:

`curl -X POST kibana:5601/api/saved_objects/_import?createNewCopies=true -H "kbn-xsrf: true" -u "${ELASTIC_USER}:$(cat $ELASTIC_PASSWORD_FILE)" --form file=@dashboard.ndjson`

## Export dashboard from Kibana:

`curl --request POST "http://kibana:5601/api/saved_objects/_export" --header "Content-Type: application/json; Elastic-Api-Version=2023-10-31" --header "kbn-xsrf: string" -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" -d '{ "objects": [ { "type": "dashboard", "id": "c9c34bef-c32f-4870-95d3-288c00170cea" } ] }' -o /usr/share/kibana/config/dashboards/dashboard.ndjson`

## Keys on env-file

### Django settings
- DJANGO_SECRET_KEY
- DJANGO_SUPERUSER_PASSWORD

### Postgres settings
- POSTGRES_USER
- POSTGRES_DB
- POSTGRES_PASSWORD

### 42 API settings
- INTRA42_CLIENT_ID
- INTRA42_CLIENT_SECRET

### DevOps settings
- EMAIL_PASSWORD

### ELK

#### Password for the 'elastic' user (at least 6 characters)
- ELASTIC_PASSWORD

### Kibana settings
- KIBANA_REPORTING_KEY
- KIBANA_ENCRYPTION_KEY
- KIBANA_SECURITY_KEY

#### Password for the 'kibana_system' user (at least 6 characters)
- KIBANA_PASSWORD

#### SAMPLE Predefined Key only to be used in POC environments
- ENCRYPTION_KEY