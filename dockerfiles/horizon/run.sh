#!/bin/bash
echo "Setting up horizon"

HOST_NAME=${HOST_NAME:-"localhost"}

service httpd restart >/dev/null 2>&1
service memcached restart >/dev/null 2>&1


echo "Updating local_settings.py file..."
sed -i -e "s/^OPENSTACK_HOST.*/OPENSTACK_HOST = \"${HOST_NAME}\"/g" /etc/openstack-dashboard/local_settings.py


echo "Stopping horizon"
service httpd stop >/dev/null 2>&1
service memcached stop >/dev/null 2>&1

echo "Starting horizon using supervisord..."
exec /usr/bin/supervisord -n
