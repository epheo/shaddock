#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.operations import local as lrun, run, add
from fabric.api import *
from octopenstack import backend, model
import os

class InitConfig(object):

    def __init__(self, name):
        self.name = name
        self.backend = backend.Container()
        self.model = model.ConfigFile()

    def get_configfile(self):
        config = self.model.configuration

        


    @roles('mysql')
    def keystone_db_create(keystone_dbpass):
        run("CREATE DATABASE keystone;")
        run("GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY '%s';" % keystone_dbpass)
        run("GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY '%s';" % keystone_dbpass)
    
    @roles('mysql')
    def glance_db_create(glance_dbpass):
        run("CREATE DATABASE glance;")
        run("GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY '%s';" % glance_dbpass)
        run("GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY '%s';" % glance_dbpass)

    @roles('mysql')
    def nova_db_create(nova_dbpass):
        run("CREATE DATABASE nova;")
        run("GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY '%s';" % nova_dbpass)
        run("GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY '%s';" % nova_dbpass)

    @roles('keystone')
    def keystone_init(keystone_dbpass, host_ip):
        run('openstack-config --set /etc/keystone/keystone.conf database connection mysql://keystone:%s@%s/keystone' % keystone_dbpass, host_ip)

        run('ADMIN_TOKEN=$(openssl rand -hex 10)')
        run('echo $ADMIN_TOKEN')
        run('openstack-config --set /etc/keystone/keystone.conf DEFAULT admin_token $ADMIN_TOKEN')

        run('keystone-manage pki_setup --keystone-user keystone --keystone-group keystone')
        run('chown -R keystone:keystone /etc/keystone/ssl')
        run('chmod -R o-rwx /etc/keystone/ssl')

        run('su -s /bin/sh -c "keystone-manage db_sync" keystone')

    @roles('keystone')
    def keystone_register_services(host_ip):
        #Keystone
        run("keystone service-create --name=keystone --type=identity --description='OpenStack Identity'")
        run("keystone endpoint-create --service-id=$(keystone service-list | awk '/ identity / {print $2}') --publicurl=http://%s:5000/v2.0 --internalurl=http://%s:5000/v2.0 --adminurl=http://%s:35357/v2.0" % host_ip, host_ip, host_ip)
        #Glance
        run("keystone service-create --name=glance --type=image --description='OpenStack Image Service'")
        run("keystone endpoint-create --service-id=$(keystone service-list | awk '/ image / {print $2}') --publicurl=http://%s:9292 --internalurl=http://%s:9292 --adminurl=http://%s:9292" % host_ip, host_ip, host_ip)
        #Nova
        run("keystone service-create --name=nova --type=compute --description='OpenStack Compute'")
        run("keystone endpoint-create --service-id=$(keystone service-list | awk '/ compute / {print $2}') --publicurl=http://%s:8774/v2/%\(tenant_id\)s --internalurl=http://%s:8774/v2/%\(tenant_id\)s --adminurl=http://%s:8774/v2/%\(tenant_id\)s" % host_ip, host_ip, host_ip)

    @roles('glance')
    def glance_init(host_ip, glance_dbpass):
        run('openstack-config --set /etc/glance/glance-api.conf database connection mysql://glance:%s@%s/glance' % host_ip, glance_dbpass)
        run('openstack-config --set /etc/glance/glance-registry.conf database connection mysql://glance:%s@%s/glance' % host_ip, glance_dbpass)
 
        run('su -s /bin/sh -c "glance-manage db_sync" glance')

        run('openstack-config --set /etc/glance/glance-api.conf keystone_authtoken auth_uri http://%s:5000' % host_ip)
        run('openstack-config --set /etc/glance/glance-api.conf keystone_authtoken auth_host %s' % host_ip)
        run('openstack-config --set /etc/glance/glance-api.conf keystone_authtoken auth_port 35357')
        run('openstack-config --set /etc/glance/glance-api.conf keystone_authtoken auth_protocol http')
        run('openstack-config --set /etc/glance/glance-api.conf keystone_authtoken admin_tenant_name service')
        run('openstack-config --set /etc/glance/glance-api.conf keystone_authtoken admin_user glance')
        run('openstack-config --set /etc/glance/glance-api.conf keystone_authtoken admin_password %s' % glance_pass)
        run('openstack-config --set /etc/glance/glance-api.conf paste_deploy flavor keystone')
        run('openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken auth_uri http://%s:5000' % host_ip)
        run('openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken auth_host %s' % host_ip)
        run('openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken auth_port 35357')
        run('openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken auth_protocol http')
        run('openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken admin_tenant_name service')
        run('openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken admin_user glance')
        run('openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken admin_password %s' % glance_pass)
        run('openstack-config --set /etc/glance/glance-registry.conf paste_deploy flavor keystone')

    @roles('horizon')
    def horizon_init(name, environment):
        run('sed -i -e "s/^OPENSTACK_HOST.*/OPENSTACK_HOST = \"%s\"/g" /etc/openstack-dashboard/local_settings' % host_ip)
        run('sed -i -e "s/^ALLOWED_HOST.*/ALLOWED_HOST = \"\*\"/g" /etc/openstack-dashboard/local_settings')
        run('sed -i -e "s/^OPENSTACK_KEYSTONE_URL.*/OPENSTACK_KEYSTONE_URL = \"http:\/\/%s:5000\/v2.0\"/g" /etc/openstack-dashboard/local_settings' % host_ip)

    @roles('nova')
    def nova_init(name, environment):
        run('openstack-config --set /etc/nova/nova.conf database connection mysql://nova:%s@%s/nova' % nova_dbpass, host_ip)

        run('openstack-config --set /etc/nova/nova.conf DEFAULT rpc_backend qpid')
        run('openstack-config --set /etc/nova/nova.conf DEFAULT qpid_hostname %s' % host_ip)

        run('openstack-config --set /etc/nova/nova.conf DEFAULT my_ip %s' % host_ip)
        run('openstack-config --set /etc/nova/nova.conf DEFAULT vncserver_listen %s' % host_ip)
        run('openstack-config --set /etc/nova/nova.conf DEFAULT vncserver_proxyclient_address %s' % host_ip)

        run('su -s /bin/sh -c "nova-manage db sync" nova')

        run('openstack-config --set /etc/nova/nova.conf DEFAULT auth_strategy keystone')
        run('openstack-config --set /etc/nova/nova.conf keystone_authtoken auth_uri http://%s:5000' % host_ip)
        run('openstack-config --set /etc/nova/nova.conf keystone_authtoken auth_host %s' % host_ip)
        run('openstack-config --set /etc/nova/nova.conf keystone_authtoken auth_protocol http')
        run('openstack-config --set /etc/nova/nova.conf keystone_authtoken auth_port 35357')
        run('openstack-config --set /etc/nova/nova.conf keystone_authtoken admin_user nova')
        run('openstack-config --set /etc/nova/nova.conf keystone_authtoken admin_tenant_name service')
        run('openstack-config --set /etc/nova/nova.conf keystone_authtoken admin_password %s' % nova_pass)

    @roles('keystone')
    def keystone_base_create(password, domain_tld, demo_pass, glance_pass, nova_pass):
        ## Define users, tenants, and roles
        run('keystone user-create --name=admin --pass=%s --email=root@%s' % password, domain_tld)
        run('keystone role-create --name=admin')
        run('keystone tenant-create --name=admin --description="Admin Tenant"')
        run('keystone user-role-add --user=admin --tenant=admin --role=admin')
        run('keystone user-role-add --user=admin --role=_member_ --tenant=admin')
        run('keystone user-create --name=demo --pass=%s --email=demo@%s' % demo_pass, domain_tld)
        run('keystone tenant-create --name=demo --description="Demo Tenant"')
        run('keystone user-role-add --user=demo --role=_member_ --tenant=demo')
        run('keystone tenant-create --name=service --description="Service Tenant"')
        #Glance
        run('keystone user-create --name=glance --pass=%s  --email=glance@%s' % glance_pass, domain_tld)
        run('keystone user-role-add --user=glance --tenant=service --role=admin')
        #Nova
        run('keystone user-create --name=nova --pass=%s --email=nova@%s' % nova_pass, domain_tld)
        run('keystone user-role-add --user=nova --tenant=service --role=admin')

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
        ## Glance test
        run('mkdir images')
        run('wget --directory-prefix=./images http://cdn.download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img')
        run('wget --directory-prefix=./images http://uec-images.ubuntu.com/precise/current/precise-server-cloudimg-amd64-disk1.img')

        # echo "Creating image..."
        run('glance image-create --name "test-image" --disk-format qcow2 --container-format bare --is-public true < ./images/cirros-0.3.2-x86_64-disk.img')
        run('glance image-create --is-public true --disk-format qcow2 --container-format bare --name "Ubuntu" < ./images/precise-server-cloudimg-amd64-disk1.img')
        run('glance image-list')
