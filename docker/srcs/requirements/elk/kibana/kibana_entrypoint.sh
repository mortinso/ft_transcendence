#!/bin/bash

# Read the Kibana password from the secret file
export ELASTICSEARCH_PASSWORD=$(cat $ELASTICSEARCH_PASSWORD_FILE)

# Update Kibana configuration to use the generated certificates
echo -e "\nserver.ssl.enabled: true" >> config/kibana.yml
echo -e "\nserver.ssl.certificate: /usr/share/kibana/config/certs/kibana/kibana.crt" >> config/kibana.yml
echo -e "\nserver.ssl.key: /usr/share/kibana/config/certs/kibana/kibana.key" >> config/kibana.yml

# Set the encryption keys in the Kibana configuration
echo -e "\nxpack.encryptedSavedObjects.encryptionKey: $(cat $ENCRYPTED_SAVED_OBJECTS_KEY_FILE)" >> config/kibana.yml
echo -e "\nxpack.reporting.encryptionKey: $(cat $REPORTING_KEY_FILE)" >> config/kibana.yml
echo -e "\nxpack.security.encryptionKey: $(cat $SECURITY_KEY_FILE)" >> config/kibana.yml

echo -e "\nserver.publicBaseUrl: https://localhost:5601" >> config/kibana.yml

# Start Kibana
exec /usr/local/bin/kibana-docker