#!/usr/bin/env python2.7

from fabric.api import *
from fabric.state import env
import docker
import os                                                                 



def build():
    path = os.getcwd()

    run("sudo docker build -t epheo/openstack-base %s/base/" % path)
    run("sudo docker build -t epheo/os-mysql %s/mysql/" % path)
    run("sudo docker build -t epheo/os-rabbitmq %s/rabbitmq/" % path)
    run("sudo docker build -t epheo/os-keystone %s/keystone/" % path)
    run("sudo docker build -t epheo/os-glance %s/glance/" % path)
    run("sudo docker build -t epheo/os-nova %s/nova/" % path)
    run("sudo docker build -t epheo/os-horizon %s/horizon/" % path)

def install(host_name):

    host_ip             = '172.17.42.1'
    keystone_pass       = 'password'
    glance_pass         = 'password'
    nova_pass           = 'password'
    admin_token         = 'password'
    admin_password      = admin_token
    keystone_host       = host_name
    rabbitmq_host       = host_name
    rabbitmq_password   = 'password'
    mysql_pass          = 'password'
    mysql_host          = host_name
    mysql_user          = 'admin'

    run("sudo docker stop  $(sudo docker ps | grep -v 'CONTAINER'  |gawk '{print $1}') ")

    run("sudo docker run -d -p 3306:3306 -e MYSQL_PASS=%s epheo/os-mysql" % (mysql_pass))
    run("sudo docker run -d -p  5672:5672 -p 15672:15672 -e RABBITMQ_PASSWORD=%s -v /var/log/openstack/rabbitmq:/var/log/supervisor epheo/os-rabbitmq" % (rabbitmq_password))
    run("sleep 10")
    run("sudo docker run -d -p 35357:35357 -p 5000:5000 -h='keystone' -e HOST_NAME=%s -e MYSQL_DB=%s -e MYSQL_USER=%s -e MYSQL_PASSWORD=%s -e ADMIN_TOKEN=%s -e KEYSTONE_DBPASS=%s -v /var/log/openstack/keystone:/var/log/supervisor epheo/os-keystone" % (host_name,mysql_host,mysql_user,mysql_pass,admin_token,mysql_pass))
    run("sleep 5")
    run("sudo docker run -d -p 9292:9292 -h='glance' -e HOST_NAME=%s -e MYSQL_DB=%s -e MYSQL_USER=%s -e MYSQL_PASSWORD=%s -e RABBITMQ_HOST=%s -e RABBITMQ_PASSWORD=%s -e GLANCE_DBPASS=%s -v /var/log/openstack/glance:/var/log/supervisor epheo/os-glance" % (host_name,mysql_host,mysql_user,mysql_pass,rabbitmq_host,rabbitmq_password,mysql_pass))
    run("sleep 5")
    run("sudo docker run -d -p 8774:8774 -p 8775:8775 -h='nova' -e HOST_NAME=%s -e HOST_IP=%s -e MYSQL_DB=%s -e MYSQL_USER=%s -e MYSQL_PASSWORD=%s -e RABBITMQ_HOST=%s -e RABBITMQ_PASSWORD=%s -e NOVA_DBPASS=%s -e ADMIN_PASS=%s --privileged -v /var/log/openstack/nova:/var/log/supervisor epheo/os-nova" % (host_name,mysql_host,mysql_user,mysql_pass,rabbitmq_host,rabbitmq_password,mysql_pass,admin_password))
    run("sleep 5")
    run("sudo docker run -d -p 80:80 -p 11211:11211 -h='horizon' -v /var/log/openstack/horizon:/var/log/supervisor -v /var/log/openstack/apache2:/var/log/apache2 -e HOST_NAME=%s epheo/os-horizon" % (host_name))


def setup(host_name):
    run("%s/create_default_user.sh" % path)
    run("%s/keystone/create_user.sh keystone %s" % (path, host_name))
    run("%s/keystone/register_service.sh keystone %s" % (path, host_name))
    run("%s/glance/create_user.sh glance %s" % (path, host_name))
    run("%s/glance/register_service.sh glance %s" % (path,host_name))
    run("%s/nova/create_user.sh nova %s" % (path, host_name))
    run("%s/nova/register_service.sh nova %s" % (path, host_name))

def test(host_name):
    with cd('test'):
        run("%s/keystone_test.sh %s" % (path, host_name))
        run("%s/glance_test.sh %s" % (path, host_name))



def docker_deploy():
    docker_api = docker.Client(base_url='unix://var/run/docker.sock',
                 		   version='1.12',
                 		   timeout=10)
    docker_api.pull('epheo/os-nova', tag='latest')
    osnova = docker_api.create_container('epheo/os-nova', 
                                            volumes='/var/log/openstack/nova:/var/log/supervisor',
                                            name='os-nova')
    docker_api.start(es, port_bindings={8774: ('0.0.0.0', 8774), 8775: ('0.0.0.0', 8775)})

if __name__ == '__main__':
    host_name = 'node1'
    hosts = ['localhost']
    build()
    install()