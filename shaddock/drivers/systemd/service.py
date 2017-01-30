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

from shaddock.drivers.systemd.ssh import SecureShell
import sys
from docker import DockerApi


class Service(object):
    """Instance a defined container

    This class instance a Docker container depending on its
    name and model definition.
    The basics Docker methods are implemented as well as a
    Shaddock's specific one that return the information of
    the concerned container.

    Shaddock keep no tracks of any Container ID and rely on no
    databases. THe containers are retrieve from their names.
    """

    def __init__(self, svc_cfg, infos=None):
        self.cfg = svc_cfg
        self.docker_client = None
        if infos is None:
            docker_api = DockerApi(self.cfg['api_cfg'])
            self.docker_client = docker_api.connect()
        self.info = self._get_info(infos)

    def create(self):
        """Returns (dict):

        A dictionary with an image 'Id' key and a 'Warnings' key.
        """
        print('Creating container: {}'.format(self.cfg['name']))
        create = self.docker_client.create_container()
        return create
