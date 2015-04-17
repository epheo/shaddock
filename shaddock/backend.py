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

import docker
import json
from shaddock import model
import sys


class Image(object):
    def __init__(self, name, docker_host, docker_version):
        self.cfg = model.ContainerConfig(name)
        self.name = self.cfg.name
        self.docker_host = docker_host
        self.docker_version = docker_version
        self.dockerapi = docker.Client(base_url=self.docker_host,
                                       version=str(self.docker_version),
                                       timeout=10)

    def build(self, nocache):
        for line in self.dockerapi.build(path=self.cfg.path,
                                         tag=self.cfg.tag,
                                         nocache=nocache):
            jsonstream = json.loads(line.decode())
            stream = jsonstream.get('stream')
            error = jsonstream.get('error')
            if error is not None:
                print(error.rstrip())
            if stream is not None:
                print(stream.rstrip())

    def pull(self):
        print("Pulling image:".rstrip('\n')),
        for line in self.dockerapi.pull(self.cfg.tag, stream=True):
            tick = '*'
            print(tick.rstrip('\n')),


class Container(object):
    def __init__(self, service_name, docker_host, docker_version):
        # input_name can ba a tag or a name
        self.input_name = service_name
        self.cfg = model.ContainerConfig(service_name)
        self.tag = self.cfg.tag
        self.name = self.cfg.name
        self.docker_host = docker_host
        self.docker_version = docker_version
        self.dockerapi = docker.Client(base_url=self.docker_host,
                                       version=str(self.docker_version),
                                       timeout=10)
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
        c_id = self.dockerapi.create_container(
            image=self.cfg.tag,
            name=self.name,
            detach=False,
            ports=self.cfg.ports,
            environment=model.get_vars_dict(),
            volumes=self.cfg.volumes,
            hostname=self.cfg.name)
        return c_id

    def start(self):
        if self.created is False:
            container = Container(self.input_name, self.docker_host,
                                  self.docker_version)
            self.id = container.create()
        print('Starting container: {}'.format(self.name))
        self.dockerapi.start(container=self.id,
                             binds=self.cfg.binds,
                             port_bindings=self.cfg.ports_bindings,
                             privileged=self.cfg.privileged,
                             network_mode=self.cfg.network_mode)

    def stop(self):
        if self.started is True:
            print('Stopping container: {}'.format(self.name))
            self.dockerapi.stop(self.id)

    def remove(self):
        self.stop()
        if self.created is True:
            print('Removing container: {}'.format(self.name))
            self.dockerapi.remove_container(self.id)

    def restart(self):
        self.dockerapi.restart(self.id)

    def return_logs(self):
        if self.tag is not None:

            # "Fix" in order to not use the stream generator in Python2
            if (sys.version_info > (3, 0)):
                try:
                    for line in self.dockerapi.logs(
                                           container=self.id,
                                           stderr=True,
                                           stdout=True,
                                           timestamps=False,
                                           stream=True):
                        print(line.decode('utf-8').rstrip())
                except (KeyboardInterrupt, SystemExit):
                    return True
            else:

                line = self.dockerapi.logs(container=self.id,
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
        containers_list = self.dockerapi.containers(all=True)
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
                container_info = self.dockerapi.inspect_container(c_id)
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
