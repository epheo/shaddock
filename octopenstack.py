#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

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

    user                = 'octopenstack'
    path                = '%s/dockerfiles' % (os.getcwd())
    host_ip             = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    host_name           = host_ip
    admin_password      = admin_token
    keystone_host       = host_name
    rabbitmq_host       = host_name
    mysql_host          = host_nam

    services = {

        'mysql': {
            'tag': '%s/osmysql' % (user), 
            'path': '%s/mysql/' % (path),
            'ports': [(3306, 'tcp')],
            'port_bindings': {3306: ('0.0.0.0', 3306)},
            'confs': {'MYSQL_PASS': mysql_pass },
            'volumes': ['/var/log/supervisor'],
            'binds': {'/var/log/octopenstack/mysql': {'bind': '/var/log/supervisor', 'ro': False}},
            'privileged': False
            },

        'rabbitmq': {
            'tag': '%s/osrabbitmq' % (user), 
            'path': '%s/rabbitmq/' % (path),
            'ports': [(5672, 'tcp'),(15672, 'tcp')],
            'port_bindings': {5672: ('0.0.0.0', 5672), 15672: ('0.0.0.0', 15672)},
            'confs': {'RABBITMQ_PASSWORD': rabbitmq_password },
            'volumes': ['/var/log/supervisor'],
            'binds': {'/var/log/octopenstack/rabbitmq': {'bind': '/var/log/supervisor', 'ro': False}},
            'privileged': False
            },

        'glance': {
            'tag': '%s/osglance' % (user), 
            'path': '%s/glance/' % (path),
            'ports': [(9292, 'tcp')],
            'port_bindings': {9292: ('0.0.0.0', 9292)},
            'confs': {'HOST_NAME': host_name, 
                      'MYSQL_DB': mysql_host, 
                      'MYSQL_USER': mysql_user, 
                      'MYSQL_PASSWORD': mysql_pass, 
                      'RABBITMQ_HOST': rabbitmq_host, 
                      'RABBITMQ_PASSWORD': rabbitmq_password, 
                      'GLANCE_DBPASS': glance_pass
                     },
            'volumes': ['/var/log/supervisor'],
            'binds': {'/var/log/octopenstack/glance': {'bind': '/var/log/supervisor', 'ro': False}},
            'privileged': False
            },

        'horizon': {
            'tag': '%s/oshorizon' % (user), 
            'path': '%s/horizon/' % (path),
            'ports': [(80, 'tcp'),(11211, 'tcp')],
            'port_bindings': {80: ('0.0.0.0', 80), 11211: ('0.0.0.0', 11211)},
            'confs': {'HOST_NAME': host_name },
            'volumes': ['/var/log/supervisor'],
            'binds': {'/var/log/octopenstack/horizon': {'bind': '/var/log/supervisor', 'ro': False}},
            'privileged': False
            },

        'keystone': {
            'tag': '%s/oskeystone' % (user), 
            'path': '%s/keystone/' % (path),
            'ports': [(35357, 'tcp'),(5000, 'tcp')],
            'port_bindings': {35357: ('0.0.0.0', 35357), 5000: ('0.0.0.0', 5000)},
            'confs': {'HOST_NAME': host_name, 
                      'MYSQL_DB': mysql_host, 
                      'MYSQL_USER': mysql_user, 
                      'MYSQL_PASSWORD': mysql_pass, 
                      'ADMIN_TOKEN': admin_token, 
                      'KEYSTONE_DBPASS': keystone_pass
                     },
            'volumes': ['/var/log/supervisor'],
            'binds': {'/var/log/octopenstack/keystone': {'bind': '/var/log/supervisor', 'ro': False}},
            'privileged': False
            },

        'nova': {
            'tag': '%s/osnova' % (user), 
            'path': '%s/nova/' % (path),
            'ports': [(9774, 'tcp'),(8775, 'tcp')],
            'port_bindings': {8774: ('0.0.0.0', 8774), 8775: ('0.0.0.0', 8775)},
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
            'binds': {'/var/log/octopenstack/nova': {'bind': '/var/log/supervisor', 'ro': False}},
            'privileged': True
            },

#        'novacompute': {
#            'tag': '%s/osnovacompute' % (user), 
#            'path': '%s/novacompute/' % (path),
#            'confs': {'HOST_NAME': host_name },
#            'volumes': ['/var/log/supervisor'],
#            'binds': {'/var/log/octopenstack/novacompute': {'bind': '/var/log/supervisor', 'ro': False}}
#        }

#        'base': {
#            'tag': '%s/osbase' % (user), 
#            'path': '%s/base/' % (path),
#            'confs': {'HOST_NAME': host_name },
#            'volumes': ['/var/log/supervisor'],
#            'binds': {'/var/log/octopenstack/base': {'bind': '/var/log/supervisor', 'ro': False}}
#            },

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
        print('The service "%s" does not exist' % name)

    def command_not_found(self, name):
        print('The command "%s" does not exist' % action)
        print('Available commands are: build, create or start')


class Controller(object):

    def __init__(self):
        self.model          = Model()
        self.view           = View()
        self.container      = ServiceContainer()


    def exec_service_list(self, action):
        service_list = self.model.services.keys()
        self.view.service_list(service_list)

#---------- BUILD BASE FIRST ------------#
        if action=='build':

            name    ='osbase'
            tag     = '%s/osbase' % (self.model.user)
            path    = '%s/base/' % (self.model.path)
            nocache = True

            self.container.build(name, tag, path, nocache)

        else:
            pass

#---------- LOOP FOR EACH SERVICES ----------#
        for service in service_list:
            service_info = self.model.services.get(service, None)
            if service_info is not None:

                name            = service.title()
                tag             = service_info.get('tag')
                path            = service_info.get('path')
                ports           = service_info.get('ports')
                port_bindings   = service_info.get('port_bindings')
                environment     = service_info.get('confs')
                volumes         = service_info.get('volumes')
                binds           = service_info.get('binds')
                privileged      = service_info.get('privileged')
                nocache         = False

                if action=='build':
                    self.container.build(name, tag, path, nocache)

                elif action=='run':
                    id_container = self.container.create(name, tag, volumes, ports, environment)
                    self.container.start(id_container, binds, port_bindings, privileged)

                elif action=='configure':
                    self.container.create_db(name, environment)

                else:
                    self.view.command_not_found(action)

            else:
                self.view.service_not_found(name)


class ServiceContainer(object):

    def __init__(self):
        self.view           = View()

    def build(self, name, tag, path, nocache):

        action  = 'building'
        quiet   = False
        dockerfile = '%s/Dockerfile' % (path)

        # DockerFile configuration: 
        # """""""""""""""""""""""""
        # All the parameters are include in the  services dict (here 
        # as environment).
        # They're replaced in the Dockerfile and provided to Docker as
        # a fileobj

        param_list = environment.keys()
        for param_key in param_list:
            param = environment.get(param_key)

            with open(dockerfile, "r") as dockerfile_template:
                template = dockerfile_template.read()

                print param_key     #TEST
                print param         #TEST
                fileobj = template.replace(param_key,param)

        path=None

        self.view.service_information(action, name, tag, path, nocache)
        for line in docker_api.build(path, tag, quiet, fileobj, nocache):
            print(line)


    def create(self, name, tag, volumes, ports, environment):
        action      = 'creating'
        command     = '/run.sh'
        user        = 'root'
        mem_limit   = '0'
        hostname    = name
        detach      = False
        stdin_open  = False
        tty         = False

        self.view.service_information(action, tag, command, hostname, user, ports, mem_limit, environment, volumes, name)
        id_container = docker_api.create_container(tag, command, hostname, user, detach, ports, environment, volumes, name)
        return id_container

    def start(self, id_container, binds, port_bindings, privileged):
        action            = 'starting'
        publish_all_ports = True

        self.view.service_information(action, id_container, port_bindings, privileged)
        docker_api.start(id_container, binds, port_bindings, publish_all_ports, links, privileged)
        
    def get_info(self, tag):

        # Retrieve existing containers informations:
        # """"""""""""""""""""""""""""""""""""""""""
        # First retrieve all the instances IDs, 
        # Get informations for the returned IDs 
        # And check for a match with a known tag.
        #
        # Then get instances informations in the dictionary for 
        # the matching one.
        #
        # Maybe it will be usefull to store returned information
        # in the 'services' dict?

        containers_list = docker_api.containers()

        for containers in containers_list:
            c_id = containers.get('Id')
            container_infos = docker_api.inspect_container(c_id)

            config = container_infos.get('Config')
            if config.get('Image')==tag:
                network  = container_infos.get('NetworkSettings')

                ipaddr   = network.get('IPAddress')
                dockerid = c_id
                hostname = config.get('Hostname')


    def stop(tag):
        c_id = self.get_info.dockerid(tag)
        docker_api.stop(c_id)

    def rm(tag):
        c_id = self.get_info.dockerid(tag)
        docker_api.stop(c_id)
        docker_api.remove_container(c_id)

    def create_db(self, name, environment):
#        import MySQLdb

        print environment

#        db = MySQLdb.connect(host,user,passwd,db)
#        cur = db.cursor() 

#        cur.execute("CREATE DATABASE %s;" % (name))
#        cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'localhost' IDENTIFIED BY '${GLANCE_DBPASS}';")
#        cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'${HOST_NAME}' IDENTIFIED BY '${GLANCE_DBPASS}';")
#        cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'%' IDENTIFIED BY '${GLANCE_DBPASS}'")

#    def config_files():

if __name__ == '__main__':

    action     = str(sys.argv[1])
    docker_api = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
    controller = Controller()

    controller.exec_service_list(action)
