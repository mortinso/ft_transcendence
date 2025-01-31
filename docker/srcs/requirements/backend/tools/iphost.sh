#!/bin/bash

# Your script logic here
IP_HOST=$(hostname -I | awk '{print $1}')
if [ -z "$IP_HOST" ]; then
    echo "Failed to retrieve local IP address."
    exit 1
else
    echo "IP_HOST: $IP_HOST"
fi

# Path to .env
ENV_FILE="srcs/.env"

# Check if .env file exists
if [ -f "$ENV_FILE" ]; then
    # Remove existing line with IP_HOST if present
    sed -i '/^IP_HOST=/d' "$ENV_FILE"
    # Add a new line with IP_HOST
    echo -e "\nIP_HOST=\"$IP_HOST\"" >> "$ENV_FILE"
    # echo "IP_HOST added to $ENV_FILE"
else
    echo "File $ENV_FILE not found."
    exit 1
fi

# echo "Finished iphost.sh script"