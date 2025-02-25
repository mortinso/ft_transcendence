#!/bin/bash
set -e

mkdir -p docker/secrets

####### DJANGO SECRETS ########

if [ ! -f docker/secrets/django_superuser_password.txt ]; then
    echo -n "admin" > docker/secrets/django_superuser_password.txt
fi

if [ ! -f docker/secrets/django_secret_key.txt ]; then
    echo -n '$cfqq-xvjr=5ea=d1%j+&_w49tr$#+^p_ulao_mumf83!5@$j_' > docker/secrets/django_secret_key.txt
fi

####### POSTGRES SECRETS ########

if [ ! -f docker/secrets/postgres_password.txt ]; then
    echo -n "admin" > docker/secrets/postgres_password.txt
fi

####### EMAIL SECRETS ########

if [ ! -f docker/secrets/email_host_password.txt ]; then
    echo -n "lpso ireq tocn usrs" > docker/secrets/email_host_password.txt
fi

####### INTRA42 SECRETS ########

if [ ! -f docker/secrets/intra42_redirect_uri.txt ]; then
    echo -n 'https://ft-transcendence.com/api/oauth/login/redirect' > docker/secrets/intra42_redirect_uri.txt
fi

if [ ! -f docker/secrets/intra42_auth_url.txt ]; then
    echo -n 'https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-6f95013ff80b03205f10c6858a27d612b0471205a3be99b15a164083c741aa4f&redirect_uri=https%3A%2F%2Fft-transcendence.com%2Fapi%2Foauth%2Flogin%2Fredirect&response_type=code' > docker/secrets/intra42_auth_url.txt
fi

if [ ! -f docker/secrets/intra42_client_id.txt ]; then
    echo -n 'u-s4t2ud-6f95013ff80b03205f10c6858a27d612b0471205a3be99b15a164083c741aa4f' > docker/secrets/intra42_client_id.txt
fi

if [ ! -f docker/secrets/intra42_client_secret.txt ]; then
    echo -n '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' > docker/secrets/intra42_client_secret.txt
fi

####### KIBANA SECRETS ########

if [ ! -f docker/secrets/kibana_encryption_key.txt ]; then
    echo -n '3d82e12880b24fb615b2c47da27be64a' > docker/secrets/kibana_encryption_key.txt
fi

if [ ! -f docker/secrets/kibana_password.txt ]; then
    echo -n 'kibana_password' > docker/secrets/kibana_password.txt
fi

if [ ! -f docker/secrets/kibana_reporting_ley.txt ]; then
    echo -n '41d74f160763015437ad583937f9a561' > docker/secrets/kibana_reporting_ley.txt
fi

if [ ! -f docker/secrets/kibana_security_key.txt ]; then
    echo -n '01842ab4dbbb8692153c78a52ab5c1eb' > docker/secrets/kibana_security_key.txt
fi

####### ELASTICSEARCH SECRETS ########

if [ ! -f docker/secrets/elasticsearch_password.txt ]; then
    echo -n 'elastic_password' > docker/secrets/elasticsearch_password.txt
fi

echo "Secrets generated successfully!"