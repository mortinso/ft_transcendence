#! /bin/sh

cd transcendence

export DJANGO_SUPERUSER_PASSWORD=$(cat /run/secrets/django_superuser_password);

pip install -r requirements.txt

cd backend

python3 manage.py collectstatic --noinput

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser --username admin --email mail@mail.com --noinput

echo "backend starting"

exec "$@"