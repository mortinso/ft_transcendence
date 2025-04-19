#!/bin/bash

# Update Kibana configuration to use the generated certificates
if ! grep -q "^server.ssl.enabled:" config/kibana.yml; then
echo -e "\nserver.ssl.enabled: true" >> config/kibana.yml
fi
if ! grep -q "^server.ssl.certificate: /usr/share/kibana/config/certs/kibana/kibana.crt" config/kibana.yml; then
echo -e "\nserver.ssl.certificate: /usr/share/kibana/config/certs/kibana/kibana.crt" >> config/kibana.yml
fi
if ! grep -q "^server.ssl.key: /usr/share/kibana/config/certs/kibana/kibana.key" config/kibana.yml; then
echo -e "\nserver.ssl.key: /usr/share/kibana/config/certs/kibana/kibana.key" >> config/kibana.yml
fi
# Set the encryption keys in the Kibana configuration
if ! grep -q "^xpack.encryptedSavedObjects.encryptionKey: ${ENCRYPTED_SAVED_OBJECTS_KEY}" config/kibana.yml; then
echo -e "\nxpack.encryptedSavedObjects.encryptionKey: ${ENCRYPTED_SAVED_OBJECTS_KEY}" >> config/kibana.yml
fi
if ! grep -q "^xpack.reporting.encryptionKey: ${REPORTING_KEY}" config/kibana.yml; then
echo -e "\nxpack.reporting.encryptionKey: ${REPORTING_KEY}" >> config/kibana.yml
fi
if ! grep -q "^xpack.security.encryptionKey: ${SECURITY_KEY}" config/kibana.yml; then
echo -e "\nxpack.security.encryptionKey: ${SECURITY_KEY}" >> config/kibana.yml
fi
if ! grep -q "^server.publicBaseUrl: https://localhost:5601" config/kibana.yml; then
echo -e "\nserver.publicBaseUrl: https://localhost:5601" >> config/kibana.yml
fi
# Start Kibana
exec /usr/local/bin/kibana-docker