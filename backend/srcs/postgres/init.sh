#!/bin/bash

# Replace placeholders in init.template.sql with environment variable values
sed -e "s/\${POSTGRES_DJANGO_USER}/$POSTGRES_DJANGO_USER/g" \
    -e "s/\${POSTGRES_DJANGO_PASSWORD}/$POSTGRES_DJANGO_PASSWORD/g" \
    -e "s/\${POSTGRES_DJANGO_DB}/$POSTGRES_DJANGO_DB/g" \
    /docker-entrypoint-initdb.d/init.template.sql.ignore > /tmp/init_processed.sql

# Execute the processed SQL file
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --file=/tmp/init_processed.sql