#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import socket

class Dico(object):

    def __init__(self, service_name):
        self.name = service_name
        self.config_path = '/etc/octopenstack'
        self.dictionary = self.make_service_dictionary()
        self.tag = self.dictionary.get('tag')
        self.path = self.dictionary.get('path')
        self.ports = self.dictionary.get('ports')
        self.port_bindings = self.dictionary.get('port_bindings')
        self.config = self.dictionary.get('confs')
        self.volumes = self.dictionary.get('volumes')
        self.binds = self.dictionary.get('binds')
        self.privileged = self.dictionary.get('privileged')

    def make_service_dictionary(self):
        services_dic = open('%s/services.yml' % self.config_path, "r")
        services_dic = services_dic.read()
        services_dic = yaml.load(services_dic)
        services_keys = services_dic.keys()

        config_dic = open('%s/configuration.yml' % self.config_path, "r")
        config_dic = config_dic.read()
        config_dic = yaml.load(config_dic)
        configuration = config_dic.get('services_config')
        user = config_dic.get('user')
        self.nocache = config_dic.get('nocache')

        for service in services_keys:
            if service.lower() == self.name:
                service_info = services_dic.get(self.name, None)
                ports = service_info.get('ports')
                volumes = service_info.get('volumes')
                self.privileged = service_info.get('privileged')

        try:
           ports
        except NameError:
            print("Unrecognized service name")
            exit(0)

        service_dic = {}

        service_dic['tag'] = '%s/oos-%s' % (user, self.name)
        service_dic['path'] = '%s/%s' % (self.config_path, self.name)

        ports_list = []
        ports_bind_dico = {}

        for port in ports:
            ports_list.append((port, 'tcp'))
            ports_bind_dico[port] = ('0.0.0.0', port)

        service_dic['ports'] = ports_list
        service_dic['port_bindings'] = ports_bind_dico

        volumes_list = []
        binds_dico = {}
        for volume in volumes.keys():
          volumes_list.append(volume)
          bind = volumes.get(volume)
          binds_dico[bind] = {'bind': volume, 'ro': False}

        service_dic['volumes'] = volumes_list
        service_dic['binds'] = binds_dico
        service_dic['confs'] = configuration

        return service_dic

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
