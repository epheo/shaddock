#!/bin/bash

export HOST_NAME=$1

keystone --os-username=admin --os-password=password --os-auth-url=http://${HOST_NAME}:35357/v2.0 token-get
keystone --os-username=admin --os-password=password --os-tenant-name=admin  --os-auth-url=http://${HOST_NAME}:35357/v2.0 token-get
#export OS_SERVICE_TOKEN=password
#export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0

export OS_USERNAME=admin
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://${HOST_NAME}:5000/v2.0/
export OS_PASSWORD=password
echo "keystone service-list"
keystone service-list 
echo "keystone user-list"
keystone user-list
echo "keystone tenant-list"
keystone tenant-list
echo "keystone user-role-list"
keystone user-role-list --user admin --tenant admin
echo "keystone token-get"
keystone token-get
