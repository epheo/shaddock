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
from octopenstack import view, model


class Image(object):

    def __init__(self, service_name):
        self.view = view.View()
        self.name = service_name
        self.dico = model.Dico(self.name)
        self.configfile = model.ConfigFile()

        self.dockerapi = docker.Client(base_url=self.configfile.docker_url,
                                       version=self.configfile.docker_version,
                                       timeout=10)

    def build(self):
        action = 'building'
        quiet = False
        rm = False
        stream = False
        timeout = None
        custom_context = False
        fileobj = None

        if self.dico.tag is not None:
            self.view.service_information(action,
                                          self.dico.name,
                                          self.dico.tag,
                                          self.dico.path,
                                          self.configfile.nocache)

            for line in self.dockerapi.build(self.dico.path,
                                             self.dico.tag,
                                             quiet,
                                             fileobj,
                                             self.configfile.nocache,
                                             rm,
                                             stream,
                                             timeout,
                                             custom_context):
                self.view.display_stream(line)
        else:
            print("Unrecognized service name")

    def create(self):
        action = 'creating'
        command = None
        user = 'root'
        mem_limit = '0'
        detach = False

        self.view.service_information(action,
                                      self.dico.tag,
                                      command,
                                      self.name,
                                      user,
                                      self.dico.ports,
                                      mem_limit,
                                      self.dico.config,
                                      self.dico.volumes,
                                      self.dico.name)

        id_c = self.dockerapi.create_container(self.dico.tag,
                                                       command,
                                                       self.name,
                                                       user,
                                                       detach,
                                                       self.dico.ports,
                                                       self.dico.config,
                                                       self.dico.volumes,
                                                       self.dico.name)
        return id_c


class Container(object):

    def __init__(self, service_name):
        self.view = view.View()
        self.name = service_name
        self.dico = model.Dico(self.name)
        self.tag = self.dico.tag
        self.configfile = model.ConfigFile()

        self.dockerapi = docker.Client(base_url=self.configfile.docker_url,
                                       version=self.configfile.docker_version,
                                       timeout=60)
        info = self.get_info()
        self.id = info.get('id')
        self.ip = info.get('ip')
        self.hostname = info.get('hostname')
        self.started = info.get('started')
        self.created = info.get('created')


    def start(self):
        if self.started is False and self.created is True:
            print(('Starting %s\n'
                   'id: %s') % (self.tag, self.id))

            self.dockerapi.start(self.id,
                                 self.dico.binds,
                                 self.dico.port_bindings,
                                 'True')

    def stop(self):
        if self.started is True:
            print('Stopping %s...' % self.tag)
            self.dockerapi.stop(self.id)

    def remove(self):
        self.stop()
        if self.created is True:
            print('Removing container %s' % self.id)
            self.dockerapi.remove_container(self.id)

    def restart(self):
        self.stop()
        self.start()

    def display_info(self):
        print('Name: %s' % self.name)
        print('Created: %s' % self.created)
        print('Started: %s' % self.started)
        print('IP: %s' % self.ip)
        print('ID: %s' % self.id)
        print('Tag: %s \n' % self.tag)

    def get_info(self):
        info = {}
        info['id'] = None
        info['ip'] = None
        info['hostname'] = None
        info['started'] = False
        info['created'] = False

        containers_list = self.dockerapi.containers(all=True)
        if containers_list:
            for containers in containers_list:
                c_id = containers.get('Id')
                container_info = self.dockerapi.inspect_container(c_id)

                config = container_info.get('Config')
                if config.get('Image') == self.tag:
                    network = container_info.get('NetworkSettings')
                    info['id'] = c_id
                    info['ip'] = network.get('IPAddress')
                    info['hostname'] = config.get('Hostname')
                    info['created'] = True
                    if info.get('ip'):
                        info['started'] = True
        return info