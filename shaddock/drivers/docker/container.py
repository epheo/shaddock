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

from shaddock.drivers.docker import api as dockerapi
from shaddock import model
import sys


class Container(object):
    def __init__(self, service_name, app_args):
        self.app_args = app_args
        # input_name can ba a tag or a name
        self.input_name = service_name
        self.cfg = model.ContainerConfig(service_name, self.app_args)
        self.tag = self.cfg.tag
        self.name = self.cfg.name
        self.host = self.cfg.host
        self.cluster_hosts = self.cfg.cluster_hosts

        if self.cfg.host is None:
            docker_client = dockerapi.DockerApi(self.app_args)
            self.docker_api = docker_client.api
        else:
            self.api = model.DockerConfig(self.host, self.app_args,
                    self.cluster_hosts)
            args_url = self.app_args.docker_host
            self.app_args.docker_host = self.api.url
            docker_client = dockerapi.DockerApi(self.app_args)
            self.docker_api = docker_client.api
            self.app_args.docker_host = args_url

        info = self.get_info()
        for attr in info.keys():
            setattr(self, attr, info[attr])
        # self.id = info['id']
        # self.ip = info['ip']
        # self.hostname = info['hostname']
        # self.started = info['started']
        # self.created = info['created']

    def create(self):
        print('Creating container: {}'.format(self.name))
        c_id = self.docker_api.create_container(
            image=self.cfg.tag,
            name=self.name,
            detach=False,
            ports=self.cfg.ports,
            environment=self.cfg.env,
            volumes=self.cfg.volumes,
            hostname=self.cfg.name)
        return c_id

    def start(self):
        if self.created is False:
            container = Container(self.input_name, self.app_args)
            self.id = container.create()
        print('Starting container: {}'.format(self.name))
        self.docker_api.start(container=self.id,
                              binds=self.cfg.binds,
                              port_bindings=self.cfg.ports_bindings,
                              privileged=self.cfg.privileged,
                              network_mode=self.cfg.network_mode)

    def stop(self):
        if self.started is True:
            print('Stopping container: {}'.format(self.name))
            self.docker_api.stop(self.id)

    def remove(self):
        self.stop()
        if self.created is True:
            print('Removing container: {}'.format(self.name))
            self.docker_api.remove_container(self.id)

    def restart(self):
        self.docker_api.restart(self.id)

    def return_logs(self):
        if self.tag is not None:

            # "Fix" in order to not use the stream generator in Python2
            if sys.version_info > (3, 0):
                try:
                    for line in self.docker_api.logs(
                                           container=self.id,
                                           stderr=True,
                                           stdout=True,
                                           timestamps=False,
                                           stream=True):
                        print(line.decode('utf-8').rstrip())
                except (KeyboardInterrupt, SystemExit):
                    return True
            else:
                line = self.docker_api.logs(container=self.id,
                                            stderr=True,
                                            stdout=True,
                                            timestamps=False,
                                            stream=False)
                print(line)

    def get_info(self):
        info = {}
        info['id'] = None
        info['ip'] = None
        info['hostname'] = None
        info['started'] = False
        info['created'] = False
        info['status'] = 'Not Created'
        containers_list = self.docker_api.containers(all=True)
        if containers_list:
            try:
                # One item contains "Names": ["/realname"]
                c_id, c_status = [(item['Id'], item['Status'])
                                  for item in containers_list
                                  if ("/" + self.name ==
                                      str(item['Names'][0]))][0]
            except IndexError:
                c_id = None
                c_status = 'Not Created'

            if c_id:
                container_info = self.docker_api.inspect_container(c_id)
                config = container_info['Config']
                network = container_info['NetworkSettings']
                info['started'] = container_info['State']['Running']
                info['id'] = c_id
                info['ip'] = network['IPAddress']
                info['hostname'] = config['Hostname']
                if c_status == "":
                    info['status'] = 'Created'
                else:
                    info['status'] = c_status
                info['created'] = True
        return info
