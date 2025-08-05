<h1>
	<p align="center">ft_transcendence</p>
	<img align="right" alt="Final Grade: 100/ 100%" src="https://img.shields.io/badge/-%20115%20%2F%20100-success">
</h1>
<p align="center">
	<b><i>Surprise.</b></i>
</p>
<p align="center">
	<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/mortinso/ft_transcendence">
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/mortinso/ft_transcendence">
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/mortinso/ft_transcendence">
</p>

<details>
	<summary><h2>Table of Contents</h2></summary>
<table>
<tr>
<td>

1. [Overview](https://github.com/mortinso/ft_transcendence/#overview)

	1.1. [Mandatory Part](https://github.com/mortinso/ft_transcendence/#mandatory-part)

	1.2. [Selected Modules](https://github.com/mortinso/ft_transcendence/#selected-modules)
2. [Installation](https://github.com/mortinso/ft_transcendence/#installation)

   2.1. [Requirements](https://github.com/ft_transcendence/#requirements)

   2.2. [Build Instructions](https://github.com/mortinso/ft_transcendence/#build-instructions)
3. [API Endpoints](https://github.com/mortinso/ft_transcendence/#api-endpoints)
4. [Possible Improvements](https://github.com/mortinso/ft_transcendence/#possible-improvements)
</td>
</tr>
</table>
</details>

## Overview
This project is the development of a website where users will be able to play Pong with eachother in a nice user interface. The project is divided into two parts: the [mandatory part](https://github.com/mortinso/ft_transcendence/#mandatory-part) (worth about 25% of the grade); and multiple elective supplementary [modules](https://github.com/mortinso/ft_transcendence/#selected-modules) that can replace or complete the mandatory rules.

<details><summary><h3>Mandatory Part</h3></summary>
<table>
<tr><td><b>Minimal Technical Requirements</b></td></tr>
<tr><td>

- If a backend is included, it must be written in pure Ruby (Overwritten by the Framework Module).
- Frontend developed using pure vanilla Javascript (Overwritten by the Frontend Module).
- Single-page application.
- Compatible with the latest stable up-to-date version of Google Chrome.
- The user should encounter no unhandled errors and no warnings.
- Launched with a single command line to run an autonomous Docker container.</td></tr>
<tr><td><b>Game</b></td></tr>
<tr><td>

- Users must be able to play a live Pong game against another player directly on the website, using the same keyboard.
- Users must be able to create a tournament consisting of multiple players who take turns playing against each other. It must clearly display the matchups and order of the players.
- At tournament creation, each player must input their alias. Aliases will be reset when a new tournament is started (Overwritten by the Standard User Management module).
- The tournament system organizes the participants matchmaking, and announces the next fight.
- All players must adhere to the same rules (E.g., same paddle speed), including the single-player AI (AI Opponent Module).
- Must capture the essence of the original Pong (1972).</td></tr>
<tr><td><b>Security Concerns</b></td></tr>
<tr><td>

- Any password stored in the database must be hashed.
- The website must be protected against SQL injections/XSS.
- An HTTPS connection must be enabled for all aspects related to the backend (if one is included).
- Any forms and user input must be validated, either within the base page if no backend is used or on the server side if a backend is used.</td></tr>
</table>
</details>

<details><summary><h3>Selected Modules</h3></summary>
<table>
	<tr><td colspan="2" align="center"><b>Web</b></td></tr>
	<tr><td>Framework</td>
	<td>Use the Django web framework for backend development.</td></tr>
	<tr><td>Frontend</td>
	<td>Use the Bootstrap toolkit for frontend development.</td></tr>
	<tr><td>Database</td>
	<td>The designated database for all DB instances is PostgreSQL. This choice guarantees data consistency and compatibility across all project components.</td></tr>
	<tr><td colspan="2" align="center"><b>User Management</b></td></tr>
	<tr><td>Standard User Management</td>
	<td>

- Enable a secure way for user registration and subsequent subsequent logins.
- Users can set a unique display name.
- Users can update their information, including uploading custom avatars.
- Users can add others as friends and view their online status.
- User profiles display stats (wins and losses) and a match History, accessible to logged in users.
	</td></tr>
	<tr><td>Remote Authentication</td>
	<td>Enable remote user authentication (OAuth 2.0 with 42), providing users with a secure and convenient way to access the web application.
	</td></tr>
	<tr><td colspan="2" align="center"><b>Gameplay and User Experience</b></td></tr>
	<tr><td>Second Game</td>
	<td>Expand the platform by introducing a new game, enhancing user engagement with gameplay history.</td></tr>
	<tr><td colspan="2" align="center"><b>AI-Algo</b></td></tr>
	<tr><td>AI Opponent</td>
	<td>Enhance the game by introducing an AI opponent that adds excitement and competitiveness without relying on the A* algorithm.</td></tr>
	<tr><td colspan="2" align="center"><b>Cybersecurity</b></td></tr>
	<tr><td>Two-Factor Authentication and JWT</td>
	<td>Strengthen user account security by offering Two-Factor Authentication (2FA) and enhance authentication and authorization through the use of JSON Web Tokens (JWT).</td></tr>
	<tr><td colspan="2" align="center"><b>DevOps</b></td></tr>
	<tr><td>Infrastructure Setup for Log Management</td>
	<td>Establish a powerful log management and analysis system using the ELK stack (Elasticsearch, Logstash, Kibana), enabling effective troubleshooting, monitoring, and insights into the system’s operation and performance.</td></tr>
	<tr><td colspan="2" align="center"><b>Acessibility</b></td></tr>
	<tr><td>Support All Devices</td>
	<td>Provide a consistent and user-friendly experience on all devices, maximizing accessibility and user satisfaction.</td></tr>
	<tr><td>Expanding Browser Compatibility</td>
	<td>Broaden the accessibility of the web application by supporting an additional web browser, providing users with more choices for their browsing experience.</td></tr>
	<tr><td>Multiple Languages</td>
	<td>Enhance the accessibility and inclusivity of the website by offering content in multiple languages, making it more user-friendly for a diverse international audience.</td></tr>
</table>
</details>

## Installation
### Requirements
- make
- Docker

### Build Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/mortinso/ft_transcendence.git
   ```
2. Create the `.env` file:
	```bash
	cd ft_transcendence
	touch .env
	```
3. Populate the `.env` file with the following variables and set them:
	```
	# Django
	DJANGO_SECRET_KEY=
	DJANGO_SUPERUSER_PASSWORD=

	# Postgres
	POSTGRES_USER=
	POSTGRES_DB=
	POSTGRES_PASSWORD=

	# 42 API
	INTRA42_CLIENT_ID=
	INTRA42_CLIENT_SECRET=

	# DevOps
	EMAIL_PASSWORD=

	# ELK
	# Password for the 'elastic' user (at least 6 characters)
	ELASTIC_PASSWORD=

	# Kibana
	KIBANA_REPORTING_KEY=
	KIBANA_ENCRYPTION_KEY=
	KIBANA_SECURITY_KEY=

	# Password for the 'kibana_system' user (at least 6 characters)
	KIBANA_PASSWORD=

	# SAMPLE Predefined Key only to be used in POC environments
	ENCRYPTION_KEY=
	```
4. Start the webapp:
	```bash
	make
	```
5. Open it in the browser at: `<HOST_IP>`

## API Endpoints
### Users
<table><tr><td colspan="3" align="center"><b>Listing and Updating</b></td></tr>
<tr><td>

`/api/users`</td>
<td>Lists users, except the current user.</td><td></td></tr>
<tr><td>

`/api/users/<uuid>`</td>
<td>

Retrieves user `<uuid>`, if it exists.</td><td></td></tr>
<tr><td>

`/api/users/whoami`</td>
<td>Retrieves the current user.</td><td></td></tr>
<tr><td>

`/api/users/<uuid>/edit`</td>
<td>

Update/destroy `<uuid>` if `<uuid>` is the current user, otherwise error 404.</td>
<td>

`username`, `email`, `old_password`, `password`, `confirm_password`, `first_name`, `last_name`</td></tr>
<tr><td>

`/api/users/<uuid>/add_avatar`</td>
<td>Add or update the avatar.</td>
<td>

`avatar`
</td></tr>
<tr><td colspan="3" align="center"><b>Friends</b></td></tr>
<tr><td>

`/api/users/<uuid>/invite_friend`</td>
<td>

Send friend request from `<uuid>`.</td><td></td></tr>
<tr><td>

`/api/users/<uuid>/accept_friend`</td>
<td>Accept friend request.</td><td></td></tr>
<tr><td>

`/api/users/<uuid>/remove_friend`</td>
<td>Remove friend.</td><td></td></tr>
<tr><td>

`/api/users/<uuid>/remove_friend_request`</td>
<td>Remove friend request.</td><td></td></tr>
<tr><td>

`/api/users/<uuid>/block`</td>
<td>Block user.</td><td></td></tr>
<tr><td>

`/api/users/<uuid>/unblock`</td>
<td>Unblock user.</td><td></td></tr>
<tr><td colspan="3" align="center"><b>Images</b></td></tr>
<tr><td>

`/api/users/<uuid:pk>/add_avatar/`</td>
<td>Add user avatar.</td><td></td></tr>
<tr><td>

`/api/users/<uuid:pk>/get_avatar/`</td>
<td>Get user avatar.</td><td></td></tr>
<tr><td colspan="3" align="center"><b>Auth</b></td></tr>
<tr><td>

`/api/login/`</td>
<td>Log in.</td><td></td></tr>
<tr><td>

`/api/auth/logout/`</td>
<td>Log out.</td><td></td></tr>
<tr><td>

`/api/auth/signup/`</td>
<td>Sign up.</td><td></td></tr>
<tr><td>

`/api/auth/check_otp/`</td>
<td>Confirm users one-time password.</td><td></td></tr>
<tr><td colspan="3" align="center"><b>OAuth</b></td></tr>
<tr><td>

`/api/oauth/login`</td>
<td>OAuth2 authentication.</td><td></td></tr>
<tr><td>

`/api/oauth/logout`</td>
<td>OAuth2 log out.</td><td></td></tr>
</table>

> [!IMPORTANT]
> On signup, a 6-digit one time password is sent to the users email. That password must be then sent to `/api/auth/check_otp/` as `otp`. If the OTP is valid, the page will return `200: OTP OK` and the user is created.

> [!IMPORTANT]
> If the user has 2FA enabled, when the user logs in, a 6-digit one time password is sent to the their email. That password must be then sent to `/api/auth/check_otp/` as `otp`. If the OTP is valid, the page will return the JWT.

<table>
<tr><td colspan="2" align="center"><b>OAuth</b></td></tr>
<tr><td>

`/api/<uuid:user_pk>/games/create/`</td>
<td>Creates a game and returns its info.</td></tr>
<tr><td>

`/api/<uuid:user_pk>/games/`</td>
<td>List the users game history.</td></tr>
<tr><td>

`<uuid:pk>/games/<uuid:game_pk>/edit/`</td>
<td>

Edit a specific game using its `game_id`.</td></tr>
</table>

## Possible Improvements
These are improvements that could be done without adding new Modules.
- Responsive URL subpaths (E.g., `https://www.transcendence.com/tictactoe` to open the tictactoe subpage). Currently no subpaths are supported.
- Real time notifications: This could be done using a webhook, currently the notifications are only updated when the page is refreshed.