#!/bin/bash

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
