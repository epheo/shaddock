#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from fabric.api import *
import docker
import os
import socket

class Model(object):
    keystone_pass       = 'password'
    glance_pass         = 'password'
    nova_pass           = 'password'
    admin_token         = 'password'
    rabbitmq_password   = 'password'
    mysql_pass          = 'password'
    mysql_user          = 'admin'
    user                = 'py-devstack'

    path                = os.getcwd()
    host_ip             = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    host_name           = host_ip
    admin_password      = admin_token
    keystone_host       = host_name
    rabbitmq_host       = host_name
    mysql_host          = host_name

    services = {
        'base': {
            'tag': '%s/osbase' % (user), 
            'path': '%s/base/' % (path),
            },

        'mysql': {
            'tag': '%s/osmysql' % (user), 
            'path': '%s/mysql/' % (path),
            'ports': {'3306'},
            'confs': {'MYSQL_PASS=%s' % (mysql_pass)},
            'volumes': {'/var/log/openstack/rabbitmq:/var/log/supervisor'}
            },

        'rabbitmq': {
            'tag': '%s/osrabbitmq' % (user), 
            'path': '%s/rabbitmq/' % (path),
            'ports': {'5672', '15672'},
            'confs': {'RABBITMQ_PASSWORD=%s' % (rabbitmq_password) },
            'volumes': {'/var/log/openstack/rabbitmq:/var/log/supervisor'}
            },

        'glance': {
            'tag': '%s/osglance' % (user), 
            'path': '%s/glance/' % (path),
            'ports': {'9292'},
            'confs': {'HOST_NAME=%s' % (host_name), 
                      'MYSQL_DB=%s' % (mysql_host), 
                      'MYSQL_USER=%s' % (mysql_user), 
                      'MYSQL_PASSWORD=%s' % (mysql_pass), 
                      'RABBITMQ_HOST=%s' % (rabbitmq_host), 
                      'RABBITMQ_PASSWORD=%s' % (rabbitmq_password), 
                      'GLANCE_DBPASS=%s' % (glance_pass)
                     },
            'volumes': {'/var/log/openstack/glance:/var/log/supervisor'}
            },

        'horizon': {
            'tag': '%s/oshorizon' % (user), 
            'path': '%s/horizon/' % (path),
            'ports': {'80', '11211'},
            'confs': {'HOST_NAME=%s' % (host_name) },
            'volumes': {'/var/log/openstack/horizon:/var/log/supervisor', '/var/log/openstack/apache2:/var/log/apache2'}
            },

        'keystone': {
            'tag': '%s/oskeystone' % (user), 
            'path': '%s/keystone/' % (path),
            'ports': {'35357', '5000'},
            'confs': {'HOST_NAME=%s' % (host_name), 
                      'MYSQL_DB=%s' % (mysql_host), 
                      'MYSQL_USER=%s' % (mysql_user), 
                      'MYSQL_PASSWORD=%s' % (mysql_pass), 
                      'ADMIN_TOKEN=%s' % (admin_token), 
                      'KEYSTONE_DBPASS=%s' % (keystone_pass)
                     },
            'volumes': {'/var/log/openstack/keystone:/var/log/supervisor'}
            },

        'nova': {
            'tag': '%s/osnova' % (user), 
            'path': '%s/nova/' % (path),
            'ports': {'8774', '8775'},
            'confs': {'HOST_NAME=%s' % (host_name), 
                      'HOST_IP=%s' % (host_ip), 
                      'MYSQL_DB=%s' % (mysql_host), 
                      'MYSQL_USER=%s' % (mysql_user), 
                      'MYSQL_PASSWORD=%s' % (mysql_pass), 
                      'RABBITMQ_HOST=%s' % (rabbitmq_host), 
                      'RABBITMQ_PASSWORD=%s' % (rabbitmq_password), 
                      'NOVA_DBPASS=%s' % (nova_pass), 
                      'ADMIN_PASS=%s' % (admin_password)
                     },
            'volumes': {'/var/log/openstack/nova:/var/log/supervisor'},
            'privileged': True
            },

        'novacompute': {
            'tag': '%s/osnovacompute' % (user), 
            'path': '%s/novacompute/' % (path),
            'confs': {''},
            'volumes': {''}
            },

    }

class View(object):

    def service_list(self, service_list):
        print('service LIST:')
        for service in service_list:
            print(service)
        print('')

    def service_information(self, service, service_info):
        print('service INFORMATION:')
        print('Name: %s, Tag: %s, Path: %s\n, Ports: %s\n, Confs: %s\n, Volumes:%s\n' % (service.title(), 
                                                                                         service_info.get('tag', 0), 
                                                                                         service_info.get('path', 0),
                                                                                         service_info.get('ports', 0),
                                                                                         service_info.get('confs', 0),
                                                                                         service_info.get('volumes', 0)
                                                                                        )
             )

    def service_not_found(self, service):
        print('That service "%s" does not exist' % service)


class Controller(object):

    def __init__(self):
        docker_api = docker.Client(base_url='unix://var/run/docker.sock',
                               version='1.12',
                               timeout=10)

        self.model = Model()
        self.view = View()

    def exec_service_list(self):
        service_list = self.model.services.keys()
        self.view.service_list(service_list)

        for service in service_list:
            controller.get_service_info(service)


    def get_service_info(self, service):
        service_info = self.model.services.get(service, None)
        if service_info is not None:
            self.view.service_information(service, service_info)
            #controller.service_build(service, service_info)
        else:
            self.view.service_not_found(service)

    def service_build(self, service, service_info):
        for line in docker_api.build(path = service_info.get('path', 0), tag = service_info.get('tag', 0)):
            print(line) #Print is a view, I know....


if __name__ == '__main__':

    controller = Controller()
    controller.exec_service_list()
