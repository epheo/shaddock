#!/bin/bash
echo "Setting up horizon"

HOST_NAME=${HOST_NAME:-"localhost"}

echo "Updating local_settings.py file..."
sed -i -e "s/^OPENSTACK_HOST.*/OPENSTACK_HOST = \"${HOST_NAME}\"/g" /etc/openstack-dashboard/local_settings

echo "Starting horizon using supervisord..."
exec /usr/bin/supervisord -n
