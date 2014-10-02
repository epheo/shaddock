#!/bin/bash

HOST_NAME=${HOST_NAME:-"ip-10-10-131-250-west-1.compute.internal"}
export KEYSTONE_PASS="password"
export GLANCE_PASS="password"
export NOVA_PASS="password"
export ADMIN_TOKEN="password"
export ADMIN_PASSWORD=${ADMIN_TOKEN}
export KEYSTONE_HOST=${HOST_NAME}
export RABBITMQ_HOST=${HOST_NAME}
export RABBITMQ_PASSWORD="password"
export MYSQL_PASS="password"
export MYSQL_HOST=${HOST_NAME}
export MYSQL_USER="admin"

echo "** Setting ${HOST_NAME} up defaults..."
./create_default_user.sh ${HOST_NAME}
keystone/create_user.sh keystone ${HOST_NAME}
keystone/register_service.sh keystone ${HOST_NAME}
glance/create_user.sh glance ${HOST_NAME}
glance/register_service.sh glance ${HOST_NAME}
nova/create_user.sh nova ${HOST_NAME}
nova/register_service.sh nova ${HOST_NAME}
