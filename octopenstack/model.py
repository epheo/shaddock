#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import socket

class Model(object):

    def __init__(self):
        self.services = {}
        self.make_services_dictionary(self.services)
        config_path = '/etc/octopenstack'

    def make_services_dictionary(self, services):
        config_path = '/etc/octopenstack'

        services_dic  = open('%s/services.yml' % config_path, "r")
        services_dic  = services_dic.read()
        services_dic  = yaml.load(services_dic)
        services_keys = services_dic.keys()

        config_dic    = open('%s/configuration.yml' % config_path, "r")
        config_dic    = config_dic.read()
        config_dic    = yaml.load(config_dic)
        configuration = config_dic.get('services_config')
        user          = config_dic.get('user')
        nocache       = config_dic.get('nocache')

        for service in services_keys:
            service_info = services_dic.get(service, None)
            if service_info is not None:

                name            = service.title()
                ports           = service_info.get('ports')
                volumes         = service_info.get('volumes')
                binds           = service_info.get('binds')
                privileged      = service_info.get('privileged')

                self.make_service(name, ports, volumes, binds, privileged, services, configuration, user, nocache, config_path)


    def make_service(self, name, ports, volumes, binds, privileged, services, configuration, user, nocache, config_path):
        #  Final dictionary should be like:
        #  'glance': {
        #      'tag': '%s/osglance' % (user), 
        #      'path': '%s/glance/' % (path),
        #      'ports': [(9292, 'tcp')],
        #      'port_bindings': {9292: ('0.0.0.0', 9292)},
        #      'confs': {'HOST_NAME': host_name, 
        #                'MYSQL_DB': mysql_host, 
        #                'MYSQL_USER': mysql_user, 
        #                'MYSQL_PASSWORD': mysql_pass, 
        #                'RABBITMQ_HOST': rabbitmq_host, 
        #                'RABBITMQ_PASSWORD': rabbitmq_password, 
        #                'GLANCE_DBPASS': glance_pass
        #               },
        #      'volumes': ['/var/log/supervisor'],
        #      'binds': {'/var/log/octopenstack/glance': {'bind': '/var/log/supervisor', 'ro': False}},
        #      'privileged': False
        #      },

        name            = name.lower()
        self.user       = user
        self.nocache    = nocache
        #host_ip             = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

        service_dic = {}
        self.path   =  config_path

        ## Register Tag and Path
        service_dic['tag'] = '%s/oos-%s' % (self.user, name)
        service_dic['path'] = '%s/%s' % (self.path, name)

        ## Register Ports and ports bindings
        ports_list=[]
        ports_bind_dico={}

        for port in ports:
          ports_list.append((port, 'tcp'))
          ports_bind_dico[port] = ('0.0.0.0', port)

        service_dic['ports'] = ports_list
        service_dic['port_bindings'] = ports_bind_dico

        ## Register volumes and binds
        volumes_list=[]
        binds_dico={}
        for volume in volumes.keys():
          volumes_list.append(volume)
          bind = volumes.get(volume)
          binds_dico[bind] = {'bind': volume, 'ro': False}

        service_dic['volumes'] = volumes_list
        service_dic['binds'] = binds_dico

        service_dic['confs'] = configuration

        #Register all dic in an other one.
        services[name] = service_dic