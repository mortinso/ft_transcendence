#! /bin/sh

cd transcendence

export INTRA42_CLIENT_ID=$(cat $INTRA42_CLIENT_ID_FILE)
export INTRA42_CLIENT_SECRET=$(cat $INTRA42_CLIENT_SECRET_FILE)

if [ "$DEBUG" = "1" ]; then
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

if [ "$DEBUG" = "1" ]; then
    exec python3 manage.py runserver 0.0.0.0:8000
else
    exec gunicorn --bind 0.0.0.0:8000 backend.wsgi
fi