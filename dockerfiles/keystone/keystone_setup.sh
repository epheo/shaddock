#!/bin/bash

export OS_SERVICE_TOKEN=password
#export OS_USERNAME=keystone
#export OS_PASSWORD=password
#export OS_TENANT_NAME=myproject
export OS_AUTH_URL=http://10.10.128.99:5000/v2.0/
export OS_IDENTITY_API_VERSION=2.0
export OS_SERVICE_ENDPOINT=http://10.10.128.99:35357/v2.0

keystone tenant-create --name=admin --description="Admin Tenant"
keystone tenant-create --name=service --description="Service Tenant"
keystone user-list
keystone user-create --name=admin --pass=password --email=admin@nirmata.com
keystone role-create --name=admin
keystone user-role-add --user=admin --tenant=admin --role=admin
keystone service-create --name=keystone --type=identity  --description="Keystone Identity Service"
keystone endpoint-create --service-id=4e44b185fdc54a0f981527b643814d35 --publicurl=http://10.10.128.99:5000/v2.0 --internalurl=http:///10.10.128.99:5000/v2.0 --adminurl=http://10.10.128.99:35357/v2.0
