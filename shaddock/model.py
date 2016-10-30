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

import re
import yaml


class TemplateFileError(Exception):
    pass


def get_services_list(app_args):
    template_file = app_args.template_file
    if template_file is None:
        raise NameError("You should specify a template file with -f")
    with open(template_file) as f:
        services_list = yaml.load(f)
    return services_list


class ContainerConfig(object):
    def __init__(self, name, app_args):
        self.app_args = app_args
        self.images_dir = self.app_args.images_dir
        # This one matches anything in the form of "something/something"
        # with something beeing anything not containing slashs or spaces.
        if re.match("^[^\s/]+/[^\s/]+$", name):
            self.tag = name
            self.name = name.split('/')[1]
            self.path = '{}/{}'.format(self.images_dir, self.tag)
            self.ports = None
            self.ports_bindings = None
            self.volumes = None
            self.binds = None
            self.network_mode = 'bridge'
            self.privileged = None
        else:
            self.__construct(name)

    def __construct(self, name):
        template_file = self.app_args.template_file
        services_list = get_services_list(self.app_args)
        try:
            service = [svc for svc in services_list if
                       svc['name'] == name]
            if len(service) > 1:
                raise TemplateFileError(
                    "There is more than one definition matching"
                    " 'name: {}' in your {}".format(name, template_file))
            service = service[0]
        except IndexError:
            raise TemplateFileError(
                "There is no container definition containing"
                " 'name: {}' in your {}".format(name, template_file))
        except KeyError:
            raise TemplateFileError(
                "At least one container definition in your"
                " {} is missing the name property".format(template_file))

        self.name = name
        try:
            self.tag = service['image']
        except KeyError:
            raise TemplateFileError(
                "Container definition of: '{}' in your {} is"
                " missing the image property".format(name, template_file))

        self.privileged = service.get('privileged')
        self.env = service.get('env')
        self.path = '{}/{}'.format(self.images_dir, self.tag.split(":")[0])

        try:
            self.network_mode = service['network_mode']
        except KeyError:
            self.network_mode = 'bridge'

        self.ports = []
        self.ports_bindings = {}
        ports = service.get('ports')
        if ports is not None:
            for port in ports:
                self.ports.append((port, 'tcp'))
                self.ports_bindings[port] = ('0.0.0.0', port)

        self.volumes = []
        self.binds = {}
        tpl_volumes = service.get('volumes')
        if tpl_volumes is not None:
            try:
                for volume in tpl_volumes:
                    self.volumes.append(volume['mount'])
                    self.binds[volume['host_dir']] = {'bind': volume['mount'],
                                                      'ro': False}
            except KeyError:
                raise TemplateFileError(
                    "A container's volume definition in your"
                    " {} is missing the mount or host_dir"
                    " property".format(template_file))

        #  The returned object will look like:
        #      'name': 'nova',
        #      'tag': 'shaddock/nova',
        #      'path': '/var/lib/shaddock/images/shaddock/nova',
        #      'ports': [(8774, 'tcp'), (8775, 'tcp')],
        #      'ports_bindings': {8774: ('0.0.0.0', 8774),
        #                        8775: ('0.0.0.0', 8775)},
        #      'volumes': ['/var/log/nova'],
        #      'binds': {'/var/log/nova':
        #                {'bind': '/var/log/shaddock/nova', 'ro': False}},
        #      'privileged': True,
        #      'network_mode': None
        #      },
