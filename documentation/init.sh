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

keystone user-create --name=admin --pass=${ADMIN_PASSWORD} --email=admin@octopenstack.eu
keystone role-create --name=admin
keystone user-role-add --user=admin --tenant=admin --role=admin
keystone user-role-add --user=admin --role=_member_ --tenant=admin

keystone user-create --name=demo --pass=demo --email=demo@octopenstack.eu
keystone user-role-add --user=demo --role=_member_ --tenant=demo

echo "=> Done!"

## Keystone create user
SERVICE=$1

HOST_NAME=${HOST_NAME:-$2}
KEYSTONE_PASS=${KEYSTONE_PASS:-"password"}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}

export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0
export OS_SERVICE_TOKEN=${ADMIN_TOKEN}

echo "=> Creating ${SERVICE} user"
keystone user-create --name=${SERVICE} --pass=${KEYSTONE_PASS} --email=keystone@example.com 
keystone user-role-add --user=${SERVICE} --tenant=service --role=admin
echo "=> Done!"

## Keystone register service
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

## Glance create user
SERVICE=$1

HOST_NAME=${HOST_NAME:-$2}
GLANCE_PASS=${GLANCE_PASS:-"password"}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}

export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0
export OS_SERVICE_TOKEN=${ADMIN_TOKEN}

echo "=> Creating ${SERVICE} user"
keystone user-create --name=${SERVICE} --pass=${GLANCE_PASS} --email=glance@example.com 
keystone user-role-add --user=${SERVICE} --tenant=service --role=admin
echo "=> Done!"

## Glance register service
SERVICE=$1

HOST_NAME=${HOST_NAME:-$2}
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


## Nova create user
SERVICE=$1

HOST_NAME=${HOST_NAME:-$2}
NOVA_PASS=${NOVA_PASS:-"password"}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}

export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0
export OS_SERVICE_TOKEN=${ADMIN_TOKEN}

echo "=> Creating ${SERVICE} user"
keystone user-create --name=${SERVICE} --pass=${NOVA_PASS} --email=nova@example.com 
keystone user-role-add --user=${SERVICE} --tenant=service --role=admin
echo "=> Done!"


## Nova register service
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


## Keystone test
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


## Glance test
export HOST_NAME=$1

export OS_SERVICE_TOKEN=password
export OS_SERVICE_ENDPOINT=http://${HOST_NAME}:35357/v2.0

export OS_USERNAME=admin
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://${HOST_NAME}:5000/v2.0/
export OS_PASSWORD=password

echo "Download images"
sudo mkdir images
sudo wget --directory-prefix=./images http://cdn.download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img
sudo wget --directory-prefix=./images http://uec-images.ubuntu.com/precise/current/precise-server-cloudimg-amd64-disk1.img

echo "Creating image..."
glance image-create --name "test-image" --disk-format qcow2 --container-format bare --is-public true < ./images/cirros-0.3.2-x86_64-disk.img
glance image-create --is-public true --disk-format qcow2 --container-format bare --name "Ubuntu" < ./images/precise-server-cloudimg-amd64-disk1.img
glance image-list
