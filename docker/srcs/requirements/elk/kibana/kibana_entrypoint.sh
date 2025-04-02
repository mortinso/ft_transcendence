#!/bin/bash

# Update Kibana configuration to use the generated certificates
echo -e "\nserver.ssl.enabled: true" >> config/kibana.yml
echo -e "\nserver.ssl.certificate: /usr/share/kibana/config/certs/kibana/kibana.crt" >> config/kibana.yml
echo -e "\nserver.ssl.key: /usr/share/kibana/config/certs/kibana/kibana.key" >> config/kibana.yml

# Set the encryption keys in the Kibana configuration
echo -e "\nxpack.encryptedSavedObjects.encryptionKey: ${ENCRYPTED_SAVED_OBJECTS_KEY}" >> config/kibana.yml
echo -e "\nxpack.reporting.encryptionKey: ${REPORTING_KEY}" >> config/kibana.yml
echo -e "\nxpack.security.encryptionKey: ${SECURITY_KEY}" >> config/kibana.yml

echo -e "\nserver.publicBaseUrl: https://localhost:5601" >> config/kibana.yml

# Start Kibana
exec /usr/local/bin/kibana-docker