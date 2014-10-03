#!/usr/bin/env python27
# -*- coding: utf-8 -*-
#from fabric.api import *
import docker
import os
import socket
import sys

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
            'ports': {3306: ('0.0.0.0', 3306)},
            'confs': {'MYSQL_PASS': mysql_pass },
            'volumes': ['/var/log/supervisor'],
            'binds': { '/var/log/openstack/mysql': { 'bind': '/var/log/supervisor', 'ro': False } }
            },

        'rabbitmq': {
            'tag': '%s/osrabbitmq' % (user), 
            'path': '%s/rabbitmq/' % (path),
            'ports': {5672: ('0.0.0.0', 5672), 15672: ('0.0.0.0', 15672)},
            'confs': {'RABBITMQ_PASSWORD': rabbitmq_password },
            'volumes': ['/var/log/supervisor'],
            'binds': { '/var/log/openstack/rabbitmq': { 'bind': '/var/log/supervisor', 'ro': False } }
            },

        'glance': {
            'tag': '%s/osglance' % (user), 
            'path': '%s/glance/' % (path),
            'ports': {9292: ('0.0.0.0', 9292)},
            'confs': {'HOST_NAME': host_name, 
                      'MYSQL_DB': mysql_host, 
                      'MYSQL_USER': mysql_user, 
                      'MYSQL_PASSWORD': mysql_pass, 
                      'RABBITMQ_HOST': rabbitmq_host, 
                      'RABBITMQ_PASSWORD': rabbitmq_password, 
                      'GLANCE_DBPASS': glance_pass
                     },
            'volumes': ['/var/log/supervisor'],
            'binds': { '/var/log/openstack/glance': { 'bind': '/var/log/supervisor', 'ro': False } },
            },

        'horizon': {
            'tag': '%s/oshorizon' % (user), 
            'path': '%s/horizon/' % (path),
            'ports': {80: ('0.0.0.0', 80), 11211: ('0.0.0.0', 11211)},
            'confs': {'HOST_NAME': host_name },
            'volumes': ['/var/log/supervisor'],
            'binds': { '/var/log/openstack/horizon': { 'bind': '/var/log/supervisor', 'ro': False } }
            },

        'keystone': {
            'tag': '%s/oskeystone' % (user), 
            'path': '%s/keystone/' % (path),
            'ports': {35357: ('0.0.0.0', 35357), 5000: ('0.0.0.0', 5000)},
            'confs': {'HOST_NAME': host_name, 
                      'MYSQL_DB': mysql_host, 
                      'MYSQL_USER': mysql_user, 
                      'MYSQL_PASSWORD': mysql_pass, 
                      'ADMIN_TOKEN': admin_token, 
                      'KEYSTONE_DBPASS': keystone_pass
                     },
            'volumes': ['/var/log/supervisor'],
            'binds': { '/var/log/openstack/keystone': { 'bind': '/var/log/supervisor', 'ro': False } }
            },

        'nova': {
            'tag': '%s/osnova' % (user), 
            'path': '%s/nova/' % (path),
            'ports': {8774: ('0.0.0.0', 8774), 8775: ('0.0.0.0', 8775)},
            'confs': {'HOST_NAME': host_name, 
                      'HOST_IP': host_ip, 
                      'MYSQL_DB': mysql_host, 
                      'MYSQL_USER': mysql_user, 
                      'MYSQL_PASSWORD': mysql_pass, 
                      'RABBITMQ_HOST': rabbitmq_host, 
                      'RABBITMQ_PASSWORD': rabbitmq_password, 
                      'NOVA_DBPASS': nova_pass, 
                      'ADMIN_PASS': admin_password
                     },
            'volumes': ['/var/log/supervisor'],
            'binds': { '/var/log/openstack/nova': { 'bind': '/var/log/supervisor', 'ro': False } },
            'privileged': True
            },

        'novacompute': {
            'tag': '%s/osnovacompute' % (user), 
            'path': '%s/novacompute/' % (path),
            'confs': {''},
            'volumes': ['/var/log/supervisor'],
            'binds': { '/var/log/openstack/novacompute': { 'bind': '/var/log/supervisor', 'ro': False } }
        }

    }

class View(object):

    def service_list(self, service_list):
        print('service LIST:')
        for service in service_list:
            print(service)
        print('')

    def service_information(self, action, name, *argv):
        print('%s service %s with arguments:' % (action, name) )
        for arg in argv:
            print(arg)
        print('')


    def service_not_found(self, name):
        print('That service "%s" does not exist' % name)


class Controller(object):

    def __init__(self):
        self.model = Model()
        self.view = View()

    def exec_service_list(self, action):
        service_list = self.model.services.keys()
        self.view.service_list(service_list)

        for service in service_list:
            service_info = self.model.services.get(service, None)
            if service_info is not None:

                name            = service.title()
                tag             = service_info.get('tag')
                path            = service_info.get('path')
                port_bindings   = service_info.get('ports')
                environment     = service_info.get('confs')
                volumes         = service_info.get('volumes')
                binds           = service_info.get('binds')

                if action=='build':
                    controller.build_service_container(name, tag, path)
                else:
                    pass
                if action=='create':
                    controller.create_service_container(name, tag, volumes, environment)
                else:
                    pass
                if action=='start':
                    controller.start_service_container(name, port_bindings, binds)
                else:
                    pass
            else:
                self.view.service_not_found(name)

    def build_service_container(self, name, tag, path):
        action='building'
        self.view.service_information(action, name, tag, path)
        for line in docker_api.build(path, tag):
            print(line)

    def create_service_container(self, name, tag, volumes, environment):
        action='creating'
        self.view.service_information(action, tag, environment, volumes, name)
        id_image = docker_api.create_container(tag, environment, volumes, name)

    def start_service_container(self, name, port_bindings, binds):
        action='starting'
        self.view.service_information(action, name, port_bindings)
        id_container = docker_api.start(name, port_bindings, binds)

if __name__ == '__main__':
    action = str(sys.argv[1])
    docker_api = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
    controller = Controller()
    controller.exec_service_list(action)
