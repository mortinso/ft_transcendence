#! /bin/sh
cd transcendence

# rm -rf transcendence/venv
# python3 -m venv venv
# chmod +x ./venv/bin/activate
# ./venv/bin/activate

pip install -r requirements.txt

# python3 manage.py startapp users

# python3 manage.py startapp auth

# mv /temp/backend/* backend/
# mv /temp/users/* users
# mv /temp/auth/* auth

python3 manage.py migrate

export DJANGO_SUPERUSER_PASSWORD=$(cat /run/secrets/django_superuser_password);

python3 manage.py createsuperuser --username admin --email mail@mail.com --noinput

echo "backend starting"

exec "$@"