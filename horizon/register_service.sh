#!/bin/bash

SERVICE=$1

HOST_NAME=${HOST_NAME:-"localhost"}
KEYSTONE_HOST=${KEYSTONE_HOST:-"localhost"}
GLANCE_PASS=${GLANCE_PASS:-"password"}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}

export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0
export OS_SERVICE_TOKEN=${ADMIN_TOKEN}

echo "=> Registering ${SERVICE}"
keystone service-create --name=${SERVICE} --type=image --description="OpenStack Image Service"
keystone endpoint-create --service-id=$(keystone service-list | awk '/ image / {print $2}') \
  --publicurl=http://${HOST_NAME}:9292 \
  --internalurl=http://${HOST_NAME}:9292 \
  --adminurl=http://${HOST_NAME}:9292
echo "=> Done!"
