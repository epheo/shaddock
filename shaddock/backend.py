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
                print(error)
            if stream is not None:
                print(stream)

    def create(self):
        c_id = self.dockerapi.create_container(
            image=self.cfg.tag,
            name=self.name,
            detach=False,
            ports=self.cfg.ports,
            environment=model.get_vars_dict(),
            volumes=self.cfg.volumes,
            hostname=self.cfg.name)
        return c_id


class Container(object):
    def __init__(self, service_name, docker_host, docker_version):
        self.cfg = model.ContainerConfig(service_name)
        self.tag = self.cfg.tag
        self.name = self.cfg.name
        self.docker_host = docker_host
        self.docker_version = docker_version
        self.dockerapi = docker.Client(base_url=self.docker_host,
                                       version=str(self.docker_version),
                                       timeout=10)
        info = self.get_info()
        self.id = info['id']
        self.ip = info['ip']
        self.hostname = info['hostname']
        self.started = info['started']
        self.created = info['created']

    def start(self):
        if self.created is False:
            print('Creating container: {}'.format(self.name))
            image = Image(self.cfg.name, self.docker_host, self.docker_version)
            self.id = image.create()
        print('Starting container: {}'.format(self.name))
        self.dockerapi.start(container=self.id,
                             binds=self.cfg.binds,
                             port_bindings=self.cfg.ports_bindings,
                             privileged=self.cfg.privileged,
                             network_mode=self.cfg.network_mode)

    def stop(self):
        if self.started is True:
            print('Stopping container: {}'.format(self.tag))
            self.dockerapi.stop(self.id)

    def remove(self):
        self.stop()
        if self.created is True:
            print('Removing container: {}'.format(self.id))
            self.dockerapi.remove_container(self.id)

    def restart(self):
        self.dockerapi.restart(self.id)

    def return_logs(self):
        if self.tag is not None:
            for line in self.dockerapi.logs(
                                       container=self.id,
                                       stderr=True,
                                       stdout=True,
                                       stream=True):
                try:
                    print(str(line))
                except (KeyboardInterrupt, SystemExit):
                    return True

    def pull(self):
        for line in self.dockerapi.pull(self.tag, stream=True):
            print(json.dumps(json.loads(line), indent=4))

    def get_info(self):
        info = {}
        info['id'] = None
        info['ip'] = None
        info['hostname'] = None
        info['started'] = False
        info['created'] = False
        containers_list = self.dockerapi.containers(all=True)
        if containers_list:
            try:
                c_id = [item['Id'] for item in containers_list
                        if self.tag in item['Image']][0]
            except IndexError:
                c_id = None

            if c_id:
                container_info = self.dockerapi.inspect_container(c_id)
                config = container_info['Config']
                network = container_info['NetworkSettings']
                info['id'] = c_id
                info['ip'] = network['IPAddress']
                info['hostname'] = config['Hostname']
                info['created'] = True
                if info.get('ip'):
                    info['started'] = True
        return info
