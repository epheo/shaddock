#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2014 Thibaut Lapierre <git@epheo.eu>. All Rights Reserved.
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

from jinja2 import Template
import os.path
import re
import yaml


class TemplateFileError(Exception):
    pass


class Loader(yaml.Loader):
    """Include 

    This class change the Yaml Load fct to allow file inclusion
    using the !include keywork.
    """
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        try:
            with open(filename, 'r') as f:
                return yaml.load(f, Loader)
        except Exception:
            raise TemplateFileError(
                "The file {} you're trying to include doesn't"
                "exist.".format(filename))

Loader.add_constructor('!include', Loader.include)

def get_clusters(app_args):
    """Return a cluster list from the model.

    This method is loading the yaml model from the template files
    and return the differents clusters as a list of dicts.
    At this point the variables aren't replaced yet as they need to 
    gather values from containers execution (as the IP for exemple).
    """
    template_file = app_args.template_file
    if template_file is None:
        raise NameError("You should specify a template file with -f")
    with open(template_file) as f:
        model = yaml.load(f, Loader)
        cluster_list = []
        for cluster in model['clusters']:
            j2 = Template(str(cluster))
            if 'vars' in cluster:
                cluster_yaml = j2.render(cluster['vars'])
                cluster = yaml.load(cluster_yaml)
            cluster_list.append(cluster)
    return cluster_list


def get_services_list(app_args):
    """Return a list of services

    This method is returning a list of all the services from all
    the clusters.
    It also include in the service definition a few elements from
    the parent cluster for future use (The hosts list and 
    image dir).
    
    In the future we should change this one by "get_all_svc" and 
    create a new fct to return all the services from one specific
    cluster.
    """
    cluster_list = get_clusters(app_args)
    services_list = []
    for cluster in cluster_list:
        for service in cluster['services']:
            service['cluster_name'] = cluster['name']
            if ('host' in service and
                    'hosts' in cluster):
                service['cluster_hosts'] = cluster['hosts']
            if 'images' in cluster:
                service['img_dir'] = cluster['images']
            if 'vars' in cluster:
                service['cluster_vars'] = cluster['vars']
            services_list.append(service)
    return services_list


class Cluster(object):
    def __init__(self, cluster_name, app_args):
        clusters = get_clusters(app_args)
        #info = self.get_info()
        #for attr in info.keys():
        #    setattr(self, attr, info[attr])

class ContainerConfig(object):
    """Container definition

    This class is loading a specific service definition from 
    all the services of all the clusters and is returning as 
    arguments all the parameters that can be used as a 
    container definition depending on its name.
    """

    def __init__(self, name, app_args):
        self.app_args = app_args
        if self.app_args.images_dir:
            self.images_dir = self.app_args.images_dir
        # This one matches anything in the form of "something/something"
        # with something beeing anything not containing slashs or spaces.
        if re.match("^[^\s/]+/[^\s/]+$", name):
            self.tag = name
            self.name = name.split('/')[1]
            self.host = None
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
                    " 'name: {}' in {}".format(name, template_file))
            service = service[0]
        except IndexError:
            raise TemplateFileError(
                "There is no container definition containing"
                " 'name: {}' in {}".format(name, template_file))
        except KeyError:
            raise TemplateFileError(
                "At least one container definition in "
                " {} is missing the name property".format(template_file))

        # Global definition
        #
        self.name = name
        self.host = service.get('host')
        self.cluster_hosts = service.get('cluster_hosts')
        self.cluster_name = service.get('cluster_name')
        self.cluster_vars = service.get('cluster_vars')
        self.privileged = service.get('privileged')
        self.env = service.get('env')
        self.command = service.get('command')

        # Image dir definition
        #
        try:
            self.images_dir
        except AttributeError:
            try:
                self.images_dir = os.path.join(
                    os.path.dirname(template_file), service.get('img_dir'))
            except TypeError:
                raise TemplateFileError(
                    "Cluster definition in {} is missing the images key. "
                    "If you don't want to define a static images path in "
                    "your model you can also specify a directory to build "
                    "in with the -d cli arg.".format(template_file))
        try:
            self.tag = service['image']
        except KeyError:
            raise TemplateFileError(
                "Container definition of: '{}' in your {} is"
                " missing the image property".format(name, template_file))

        self.path = '{}/{}'.format(self.images_dir, self.tag.split(":")[0])

        # Networking definition
        #
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

        # Volume definition:
        # 
        self.volumes = []
        self.binds = {}
        tpl_volumes = service.get('volumes')
        if tpl_volumes is not None:
            try:
                for volume in tpl_volumes:
                    if len(volume['mount'].split(':')) > 1:
                        volume['mount'] = volume['mount'].split(':')[0]
                        ro = True
                    else:
                        ro = False
                    self.volumes.append(volume['mount'])
                    self.binds[volume['host_dir']] = {'bind': volume['mount'],
                                                      'ro': ro}
            except KeyError:
                raise TemplateFileError(
                    "A container's volume definition in your"
                    " {} is missing the mount or host_dir"
                    " property".format(template_file))

        # Host API Definition
        #
        try:
            self.api_cfg = [api for api in self.cluster_hosts if
                         api['name'] == self.host]
            if len(self.api_cfg) > 1:
                raise TemplateFileError(
                    "There is more than one definition matching"
                    " 'name: {}' in your model".format(name))
            self.api_cfg = self.api_cfg[0]
            
            try:
                self.api_cfg['url']
            except KeyError:
                raise TemplateFileError(
                        "Your Host definition have no matching URL")

            for key in ['cert_path', 'key_path', 'cacert_path']:
                try:
                    self.api_cfg[key]
                except KeyError:
                    self.api_cfg[key] = None

            for key in ['tls_verify', 'tls']:
               try:
                   self.api_cfg[key]
               except KeyError:
                   self.api_cfg[key] = False        

            try:
                self.api_cfg['version']
            except KeyError:
                self.api_cfg['version'] = '1.12'

        except IndexError:
            raise TemplateFileError(
                "There is no Docker Host definition containing"
                " 'name: {}' in model.".format(name))
        except KeyError:
            self.api_cfg = 'undefined'
        except TypeError:
            self.api_cfg = 'undefined'
