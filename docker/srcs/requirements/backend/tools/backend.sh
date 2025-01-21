#! /bin/sh

cd transcendence

export DJANGO_SUPERUSER_PASSWORD=$(cat $DJANGO_SUPERUSER_FILE);

if [ "$ENVIRONMENT" = "development" ]; then
    pip install -r requirements-dev.txt
else
    pip install -r requirements.txt
fi

cd backend

python3 manage.py collectstatic --noinput

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser --username admin --email mail@mail.com --noinput

echo "backend starting"

exec "$@"