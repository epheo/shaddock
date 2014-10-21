#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keystoneclient.v2_0 import client
#import MySQLdb

class InitConfig(object):
    
    def mysql(self, name, environment):

        print(environment)

        # db = MySQLdb.connect(host,user,passwd,db)
        # cur = db.cursor() 
           
        # cur.execute("CREATE DATABASE %s;" % (name))
        # cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'localhost' IDENTIFIED BY '${GLANCE_DBPASS}';")
           
        # cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'${HOST_NAME}' IDENTIFIED BY '${GLANCE_DBPASS}';")
        # cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'%' IDENTIFIED BY '${GLANCE_DBPASS}'")


    def keystone_init(self, name, environment):

        username = plop

        keystone = client.Client(username=USERNAME, password=PASSWORD, tenant_name=TENANT, auth_url=AUTH_URL)
        keystone.tenants.list()
        tenant = keystone.tenants.create(tenant_name="test", description="My new tenant!", enabled=True)
        tenant.delete()

        # keystone tenant-create --name=admin --description="Admin Tenant"
        # keystone tenant-create --name=demo --description="Demo Tenant"
        # keystone tenant-create --name=service --description="Service Tenant"

        # keystone user-create --name=admin --pass=${ADMIN_PASSWORD} --email=admin@octopenstack.eu
        # keystone role-create --name=admin
        # keystone user-role-add --user=admin --tenant=admin --role=admin
        # keystone user-role-add --user=admin --role=_member_ --tenant=admin

        # keystone user-create --name=demo --pass=demo --email=demo@epheo.com
        # keystone user-role-add --user=demo --role=_member_ --tenant=demo

    def keystone_create_user(self, name, environment):
        pass
        ## Keystone create user
        service=(keystone, glance, nova)
        #hostname = self.model.hostname
        # KEYSTONE_PASS=${KEYSTONE_PASS:-"password"}
        # ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}
        # 
        # keystone user-create --name=${SERVICE} --pass=${KEYSTONE_PASS} --email=keystone@example.com 
        # keystone user-role-add --user=${SERVICE} --tenant=service --role=admin


    def keystone_register_service(self, name, environment):
        pass
        ## Keystone register service
        service=(keystone, glance, nova)

        # HOST_NAME=${HOST_NAME:-$2}
        # KEYSTONE_HOST=${KEYSTONE_HOST:-$2}
        # KEYSTONE_PASS=${KEYSTONE_PASS:-"password"}
        # ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}
        # 
        # keystone service-create --name=${SERVICE} --type=identity --description="OpenStack Identity Service"
        # keystone endpoint-create --service-id=$(keystone service-list | awk '/ identity / {print $2}') \
        #   --publicurl=http://${HOST_NAME}:5000/v2.0 \
        #   --internalurl=http://${HOST_NAME}:5000/v2.0 \
        #   --adminurl=http://${HOST_NAME}:35357/v2.0

    def keystone_test():
        pass
        ## Keystone test
        # keystone --os-username=admin --os-password=password --os-auth-url=http://${HOST_NAME}:35357/v2.0 token-get
        # keystone --os-username=admin --os-password=password --os-tenant-name=admin  --os-auth-url=http://${HOST_NAME}:35357/v2.0 token-get
        #  
        # export OS_USERNAME=admin
        # export OS_TENANT_NAME=admin
        # export OS_AUTH_URL=http://${HOST_NAME}:5000/v2.0/
        # export OS_PASSWORD=password
        # echo "keystone service-list"
        # keystone service-list 
        # echo "keystone user-list"
        # keystone user-list
        # echo "keystone tenant-list"
        # keystone tenant-list
        # echo "keystone user-role-list"
        # keystone user-role-list --user admin --tenant admin
        # echo "keystone token-get"
        # keystone token-get

    def glance_test():
        pass
        ## Glance test
        # echo "Download images"
        # sudo mkdir images
        # sudo wget --directory-prefix=./images http://cdn.download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img
        # sudo wget --directory-prefix=./images http://uec-images.ubuntu.com/precise/current/precise-server-cloudimg-amd64-disk1.img
        #  
        # echo "Creating image..."
        # glance image-create --name "test-image" --disk-format qcow2 --container-format bare --is-public true < ./images/cirros-0.3.2-x86_64-disk.img
        # glance image-create --is-public true --disk-format qcow2 --container-format bare --name "Ubuntu" < ./images/precise-server-cloudimg-amd64-disk1.img
        # glance image-list
