#!/bin/bash

SERVICE=$1

HOST_NAME=${HOST_NAME:-$2}
KEYSTONE_HOST=${KEYSTONE_HOST:-$2}
NOVA_PASS=${NOVA_PASS:-"password"}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}

export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0
export OS_SERVICE_TOKEN=${ADMIN_TOKEN}

echo "=> Registering ${SERVICE}"
keystone service-create --name=${SERVICE} --type=compute --description="OpenStack Compute Service"
keystone endpoint-create --service-id=$(keystone service-list | awk '/ compute / {print $2}') --publicurl=http://${HOST_NAME}:8774/v2/%\(tenant_id\)s  --internalurl=http://${HOST_NAME}:8774/v2/%\(tenant_id\)s  --adminurl=http://${HOST_NAME}:8774/v2/%\(tenant_id\)s
echo "=> Done!"
