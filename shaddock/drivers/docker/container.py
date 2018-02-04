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

from copy import copy
from shaddock.drivers.docker.api import DockerApi
from docker import errors as docker_errors
import sys


class Container(object):
    """Instance a defined container

    This class instance a Docker container depending on its
    name and model definition.
    The basics Docker methods are implemented as well as a
    Shaddock's specific one that return the information of
    the concerned container.

    Shaddock keep no tracks of any Container ID and rely on no
    databases. THe containers are retrieve from their names.
    """

    def __init__(self, svc_cfg, containers_all=None):
        self.cfg = svc_cfg
        self.env = dict(self.cfg)
        # we may want to use func.__code__.co_varnames here to gather all
        # possible arguments of the docker api and compare them with cfg
        # and delete the crapy hack of the next 8 lines.
        args_to_delete = ['priority', 'depends-on', 'detach', 'api_cfg',
                          'cluster', 'images_dir', 'path', 'service_name',
                          'host']
        for arg in args_to_delete:
            try:
                del self.env[arg]
            except KeyError:
                 pass
        self.env['detach'] = self.cfg.get('detach', True)
        self.docker_client = None
        if containers_all is None:
            docker_api = DockerApi(self.cfg['api_cfg'])
            self.docker_api = docker_api.connect()
            self.docker_client = self.docker_api.containers
        self.info = self._get_info(containers_all)

    def gather_api_methods(self, func):
        return func.__code__.co_varnames

    def create(self):
        """Returns a Container object"""
        print('Creating container: {}'.format(self.cfg['name']))
        create = self.docker_client.create(**self.env)
        return create['id']

    def start(self):
        """Returns a Container object"""
        try:
            print('Starting container: {}'.format(self.cfg['name']))
            start = self.docker_client.run(**self.env)
        except docker_errors.APIError as error:
            print(error)
            print('Container {} is already running'.format(self.cfg['name']))
            return self.cfg['name']

        return start

    def stop(self):
        c = self.info.get('Container')
        if c is not None:
            print('Stopping container: {}'.format(self.cfg['name']))
            return c.stop()

    def remove(self):
        self.stop()
        c = self.info.get('Container')
        if c is not None:
            print('Removing container: {}'.format(self.cfg['name']))
            try:
                c.remove()
            except docker_errors.NotFound:
                print('Container {} does not exist'.format(self.cfg['name']))
                return True

    def restart(self):
        self.docker_client.restart(self.info['Id'])

    def return_shell(self, cmd):
        if self.cfg['image'] is not None:
            # "Fix" in order to not use the stream generator in Python2
            c = self.info.get('Container')
            if sys.version_info > (3, 0):
                try:
                    ret = c.exec_run(cmd,
                                     stderr=True,
                                     stdout=True,
                                     stream=True,
                                     )
                    for line in ret[1]:
                        print(line.decode('utf-8').rstrip())
                except (KeyboardInterrupt, SystemExit):
                    return True
            else:
                line = c.exec_run(cmd,
                                  stderr=True,
                                  stdout=True,
                                  stream=False)
                print(line[1])

    def return_logs(self):
        if self.cfg['image'] is not None:
            # "Fix" in order to not use the stream generator in Python2
            c = self.info.get('Container')
            if sys.version_info > (3, 0):
                try:
                    for line in c.logs(stderr=True,
                                       stdout=True,
                                       timestamps=True,
                                       stream=True,
                                       ):
                        print(line.decode('utf-8').rstrip())
                except (KeyboardInterrupt, SystemExit):
                    return True
            else:
                line = c.logs(stderr=True,
                              stdout=True,
                              timestamps=False,
                              stream=False)
                print(line)

    def _get_info(self, containers_all=None):
        info = {}
        if containers_all is None:
            containers_all = self.docker_client.list(all=True)
        try:
            container = [c for c in containers_all
                         if (c.name in self.cfg['service_name'])][0]

            api = DockerApi(self.cfg['api_cfg'], 'lowlevelapi')
            api = api.connect()
            infos = api.inspect_container(container.id)

            info['Container'] = container
            info['Id'] = container.id
            info['Ip'] = infos['NetworkSettings']['IPAddress']
            info['State'] = container.status

        except IndexError:
            # Container is not running
            info = {}
        return info
