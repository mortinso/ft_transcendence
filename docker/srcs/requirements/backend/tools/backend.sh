#! /bin/sh
cd transcendence

pip install -r requirements.txt
# django-admin startproject backend
cd backend

# python3 manage.py startapp users

# python3 manage.py startapp auth

# mv /temp/backend/* backend/
# mv /temp/users/* users
# mv /temp/auth/* auth

python3 manage.py collectstatic --noinput

python3 manage.py makemigrations

python3 manage.py migrate

export DJANGO_SUPERUSER_PASSWORD=$(cat /run/secrets/django_superuser_password);

python3 manage.py createsuperuser --username admin --email mail@mail.com --noinput

echo "backend starting"

exec "$@"