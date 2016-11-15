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


class ModelDefinition(object):
    """Container definition

    This class is loading the model from the yaml files and provides
    different methods to read from it more easily.
    """

    def __init__(self, app_args):
        self.app_args = app_args

        Loader.add_constructor('!include', Loader.include)

        if app_args.template_file is None:
            raise NameError("You should specify a template file with -f")
        with open(app_args.template_file) as f:
            self.model = yaml.load(f, Loader)

    def _jinja_render(template):

        return template

    def get_cluster_list(self):
        """Return a cluster list from the model.

        This method  return the differents clusters as a list of dicts.
        """

        cluster_list = []
        for cluster in self.model['clusters']:
            j2 = Template(str(cluster))
            if 'vars' in cluster:
                cluster_yaml = j2.render(cluster['vars'])
                cluster = yaml.load(cluster_yaml)
            cluster_list.append(cluster)
        return cluster_list


    def get_services_list(self):
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

        cluster_list = self.get_cluster_list()
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

    def get_cluster_args(self, name):
        clu_args = {}
        template_file = self.app_args.template_file
        cluster_list = self.get_cluster_list()

        try:
            cluster = [clu for clu in cluster_list if
                       clu['name'] == name]
            if len(cluster) > 1:
                raise TemplateFileError(
                    "There is more than one definition matching"
                    " 'name: {}' in {}".format(name, template_file))
            cluster = cluster[0]
        except IndexError:
            raise TemplateFileError(
                "There is no cluster definition containing"
                " 'name: {}' in {}".format(name, template_file))
        except KeyError:
            raise TemplateFileError(
                "At least one cluster definition in "
                " {} is missing the name property".format(template_file))

        return clu_args


    def get_service_args(self, name):
        """This method returns a dict with the service arguments.
        
        """

        svc_args = {}
        template_file = self.app_args.template_file
        services_list = self.get_services_list()

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

        # Global definition:
        #
        svc_args['name'] = name
        
        for key in ['host', 'cluster_hosts', 'cluster_name',
                'cluster_vars', 'privileged', 'env', 'command']:
            try:
                svc_args[key] = service[key]
            except KeyError:
                svc_args[key] = None


        # Image dir definition:
        #
        if self.app_args.images_dir is not None:
            svc_args['images_dir'] = self.app_args.images_dir
        else:
            try:
                svc_args['images_dir'] = os.path.join(
                    os.path.dirname(template_file), service.get('img_dir'))
            except TypeError:
                raise TemplateFileError(
                    "Cluster definition in {} is missing the images key. "
                    "If you don't want to define a static images path in "
                    "your model you can also specify a directory to build "
                    "in with the -d cli arg.".format(template_file))
        try:
            svc_args['tag'] = service['image']
        except KeyError:
            raise TemplateFileError(
                "Container definition of: '{}' in your {} is"
                " missing the image property".format(name, template_file))

        svc_args['path'] = '{}/{}'.format(svc_args['images_dir'], 
                svc_args['tag'].split(":")[0])

        # Networking definition:
        #
        try:
            svc_args['network_mode'] = service['network_mode']
        except KeyError:
            svc_args['network_mode'] = 'bridge'

        portslist = []
        ports_bindings = {}

        ports = service.get('ports')
        if ports is not None:
            for port in ports:
                portslist.append((port, 'tcp'))
                ports_bindings[port] = ('0.0.0.0', port)
        svc_args['ports'] = portslist
        svc_args['ports_bindings'] = ports_bindings

        # Volume definition:
        # 
        volumes = []
        binds = {}
        tpl_volumes = service.get('volumes')
        if tpl_volumes is not None:
            try:
                for volume in tpl_volumes:
                    if len(volume['mount'].split(':')) > 1:
                        volume['mount'] = volume['mount'].split(':')[0]
                        ro = True
                    else:
                        ro = False
                    volumes.append(volume['mount'])
                    binds[volume['host_dir']] = {'bind': volume['mount'],
                                                      'ro': ro}
            except KeyError:
                raise TemplateFileError(
                    "A container's volume definition in your"
                    " {} is missing the mount or host_dir"
                    " property".format(template_file))
        svc_args['volumes'] = volumes
        svc_args['binds'] = binds

        # Host API Definition:
        #
        #
        api_cfg = {}
        try:
            api_cfg = [api for api in svc_args['cluster_hosts'] if
                         api['name'] == svc_args['host']]
            if len(api_cfg) > 1:
                raise TemplateFileError(
                    "There is more than one definition matching"
                    " 'name: {}' in your model".format(name))
            api_cfg = api_cfg[0]
            
            try:
                api_cfg['url']
            except KeyError:
                raise TemplateFileError(
                        "Your Host definition have no matching URL")

            for key in ['cert_path', 'key_path', 'cacert_path']:
                try:
                    api_cfg[key]
                except KeyError:
                    api_cfg[key] = None

            for key in ['tls_verify', 'tls']:
               try:
                   api_cfg[key]
               except KeyError:
                   api_cfg[key] = False        

            try:
                api_cfg['version']
            except KeyError:
                api_cfg['version'] = '1.12'

        except IndexError:
            raise TemplateFileError(
                "There is no Docker Host definition containing"
                " 'name: {}' in model.".format(name))
        except KeyError:
            api_cfg = 'undefined'
        except TypeError:
            api_cfg = 'undefined'
        
        svc_args['api_cfg'] = api_cfg 

        return svc_args
