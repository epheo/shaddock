#!/usr/bin/env python27
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
            'ports': {3306: ('0.0.0.0', 3306)},
            'confs': {'MYSQL_PASS=%s' % (mysql_pass)},
            'volumes': {'/var/log/openstack/rabbitmq:/var/log/supervisor'}
            },

        'rabbitmq': {
            'tag': '%s/osrabbitmq' % (user), 
            'path': '%s/rabbitmq/' % (path),
            'ports': {5672: ('0.0.0.0', 5672), 15672: ('0.0.0.0', 15672)},
            'confs': {'RABBITMQ_PASSWORD=%s' % (rabbitmq_password) },
            'volumes': {'/var/log/openstack/rabbitmq:/var/log/supervisor'}
            },

        'glance': {
            'tag': '%s/osglance' % (user), 
            'path': '%s/glance/' % (path),
            'ports': {9292: ('0.0.0.0', 9292)},
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
            'ports': {80: ('0.0.0.0', 80), 11211: ('0.0.0.0', 11211)},
            'confs': {'HOST_NAME=%s' % (host_name) },
            'volumes': {'/var/log/openstack/horizon:/var/log/supervisor', '/var/log/openstack/apache2:/var/log/apache2'}
            },

        'keystone': {
            'tag': '%s/oskeystone' % (user), 
            'path': '%s/keystone/' % (path),
            'ports': {35357: ('0.0.0.0', 35357), 5000: ('0.0.0.0', 5000)},
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
            'ports': {8774: ('0.0.0.0', 8774), 8775: ('0.0.0.0', 8775)},
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
            'volumes': {'/var/log/openstack/novacompute:/var/log/supervisor'}
            },

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
            print arg
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
                confs           = service_info.get('confs')
                volumes         = service_info.get('volumes')

                controller.build_service_container(name, tag, path)
                controller.create_service_container(name, tag, volumes)
                controller.start_service_container(name, port_bindings, confs)

            else:
                self.view.service_not_found(name)

    def build_service_container(self, name, tag, path):
        action='building'
        self.view.service_information(action, name, tag, path)
        for line in docker_api.build(path, tag):
            print(line)


    def create_service_container(self, name, tag, volumes):
        action='creating'
        self.view.service_information(action, name, tag, volumes)
        id_image = docker_api.create_container(tag, volumes, name)


    def start_service_container(self, name, port_bindings, confs):
        action='starting'
        self.view.service_information(action, name, port_bindings, confs)
        id_container = docker_api.start(name, port_bindings)



if __name__ == '__main__':
    docker_api = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
    controller = Controller()

    action='build'
    controller.exec_service_list(action)
