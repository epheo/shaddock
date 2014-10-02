#!/bin/bash

HOST_NAME=${HOST_NAME:-$1}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}
ADMIN_PASSWORD=${ADMIN_PASSWORD:-"password"}


export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0
export OS_SERVICE_TOKEN=${ADMIN_TOKEN}

echo "=> Creating default tenant and  user"
keystone tenant-create --name=admin --description="Admin Tenant"
keystone tenant-create --name=demo --description="Demo Tenant"
keystone tenant-create --name=service --description="Service Tenant"

keystone user-create --name=admin --pass=${ADMIN_PASSWORD} --email=admin@epheo.com
keystone role-create --name=admin
keystone user-role-add --user=admin --tenant=admin --role=admin
keystone user-role-add --user=admin --role=_member_ --tenant=admin

keystone user-create --name=demo --pass=demo --email=demo@epheo.com
keystone user-role-add --user=demo --role=_member_ --tenant=demo

echo "=> Done!"
