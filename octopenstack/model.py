#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2014 Thibaut Lapierre <root@epheo.eu>. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import yaml


class ConfigFile(object):

    def __init__(self):
        self.config_path = '/etc/octopenstack'

        services_dic = open('%s/services.yml' % self.config_path, "r")
        services_dic = services_dic.read()
        services_dic = yaml.load(services_dic)
        self.services_keys = services_dic.keys()

        config_dic = open('%s/configuration.yml' % self.config_path, "r")
        config_dic = config_dic.read()
        config_dic = yaml.load(config_dic)
        self.configuration = config_dic.get('services_config')
        self.user = config_dic.get('user')
        self.nocache = config_dic.get('nocache')


class Dico(object):

    def __init__(self, service_name):
        self.name = service_name
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
        configfile = ConfigFile()

        services_dic = open('%s/services.yml' % configfile.config_path, "r")
        services_dic = services_dic.read()
        services_dic = yaml.load(services_dic)

        for service in configfile.services_keys:
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

        service_dic['tag'] = '%s/oos-%s' % (configfile.user, self.name)
        service_dic['path'] = '%s/%s' % (configfile.config_path, self.name)

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
        service_dic['confs'] = configfile.configuration

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