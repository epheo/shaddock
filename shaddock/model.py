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
from oslo.config import cfg

OPTS = [
    cfg.StrOpt('template_dir',
               default='/var/lib/shaddock',
               help='Template directory to use.'),
    cfg.StrOpt('user',
               default='shaddock',
               help='User used to build Docker images.'),
    cfg.StrOpt('nocache',
               default='False',
               help='Build images w/o cache.')
]

CONF = cfg.CONF
CONF.register_opts(OPTS)
CONF.register_cli_opts(OPTS)


def get_services_dict(template_dir=CONF.template_dir):
    with open('{}/etc/services.yml'.format(template_dir)) as f:
        services_dict = yaml.load(f)
    return services_dict


def get_vars_dict(template_dir=CONF.template_dir):
    with open('{}/etc/configuration.yml'.format(template_dir)) as f:
        vars_dict = yaml.load(f)
    return vars_dict.get('template_vars')


class ContainerConfig(object):
    def __init__(self, service_name):
        self.name = service_name

        services_dict = get_services_dict(CONF.template_dir)

        ports = None
        volumes = None
        privileged = None
        network_mode = None

        for service in services_dict.keys():
            if service.lower() == self.name:
                service_info = services_dict.get(self.name, None)
                if service_info:
                    ports = service_info.get('ports')
                    volumes = service_info.get('volumes')
                    privileged = service_info.get('privileged')
                    network_mode = service_info.get('network_mode')

        self.privileged = privileged
        self.network_mode = network_mode

        self.tag = '{}/{}'.format(CONF.user, self.name)
        self.path = '{}/template/{}'.format(CONF.template_dir, self.name)

        ports_list = []
        ports_bind_dict = {}

        if ports is not None:
            for port in ports:
                ports_list.append((port, 'tcp'))
                ports_bind_dict[port] = ('0.0.0.0', port)

        self.ports = ports_list
        self.port_bindings = ports_bind_dict

        volumes_list = []
        binds_dict = {}

        if volumes is not None:
            for volume in volumes.keys():
                volumes_list.append(volume)
                bind = volumes.get(volume)
                binds_dict[bind] = {'bind': volume, 'ro': False}

        self.volumes = volumes_list
        self.binds = binds_dict

        #  Dictionary should be like:
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
        #      'binds': {'/var/log/shaddock/glance':
        #                   {'bind': '/var/log/supervisor', 'ro': False}},
        #      'privileged': False
        #      },
