#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2016 Thibaut Lapierre <git@epheo.eu>. All Rights Reserved.
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

# from shaddock.drivers.docker import api as dockerapi
# from shaddock.model import ModelDefinition

# https://docker-py.readthedocs.io/en/latest/networks/

from shaddock.drivers.docker.api import DockerApi
from shaddock.model import ModelDefinition


class Network(object):
    """Instance a defined Docker Network

    This class instance a defined Docker network
    """

    def __init__(self, name, app_args, infos=None):
        self.app_args = app_args
        self.name = name
        model = ModelDefinition(self.app_args)
        self.cfg = model.get_network_args(self.name)
        api_cfg = self.cfg['api_cfg']
        docker_api = DockerApi(api_cfg)
        self.docker_client = docker_api.connect()

        if infos is None:
            self.info = self.get_info()
        else:
            self.info = self._get_info(infos)

    def create(self):
        """Returns (dict): The created network reference object
        """
        print('Creating network: {}'.format(self.name))
        create = self.docker_client.create_network(
            self.name,
            driver=None,
            options=None,
            ipam=None,
            check_duplicate=None,
            internal=False,
            labels=None,
            enable_ipv6=False)

        return create

    def remove(self):
        res = self.docker_client.remove_network(self.info['Id'])
        return res

    def inspect(self):
        res = self.docker_client.inspect_network(self.info['Id'])
        return res

    def connect_container(self, container):
        res = self.docker_client.connect_container_to_network(
            container,
            self.info['Id'],
            ipv4_address=None,
            ipv6_address=None,
            aliases=None,
            links=None,
            link_local_ips=None)
        return res

    def disconnect_container(self, container):
        res = self.docker_client.disconnect_container_from_network(
            container,
            self.info['Id'],
            force=False)
        return res

    def _get_info(self, networks_info=None):
        if networks_info is None:
            networks_info = self.docker_api.networks(all=True)
        try:
            # One item contains "Names": ["/realname"]
            info = [item for item in networks_info
                    if ("/" + self.name == str(
                        item['Names'][0]))][0]
        except IndexError:
            # Container is not running
            info = {}
        return info
