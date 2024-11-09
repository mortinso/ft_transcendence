#! /bin/sh

systemctl start postgresql.service

su - postgres

createuser $POSTGRES_USER

createdb $POSTGRES_DB

psql -h localhost -d mydatabase -U myuser -p <port>

exec "$@"