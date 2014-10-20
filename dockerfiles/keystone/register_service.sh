#!/bin/bash

SERVICE=$1

HOST_NAME=${HOST_NAME:-$2}
KEYSTONE_HOST=${KEYSTONE_HOST:-$2}
KEYSTONE_PASS=${KEYSTONE_PASS:-"password"}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}

export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0
export OS_SERVICE_TOKEN=${ADMIN_TOKEN}

echo "=> Registering ${SERVICE}"
keystone service-create --name=${SERVICE} --type=identity --description="OpenStack Identity Service"
keystone endpoint-create --service-id=$(keystone service-list | awk '/ identity / {print $2}') \
  --publicurl=http://${HOST_NAME}:5000/v2.0 \
  --internalurl=http://${HOST_NAME}:5000/v2.0 \
  --adminurl=http://${HOST_NAME}:35357/v2.0
echo "=> Done!"
