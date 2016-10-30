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

import json
from shaddock import model
import sys
from shaddock.drivers.docker import api as dockerapi


class Image(object):
    def __init__(self, name, app_args):
        self.app_args = app_args
        self.docker_host = app_args.docker_host
        self.docker_version = app_args.docker_version
        self.cfg = model.ContainerConfig(name, self.app_args)
        self.name = self.cfg.name
	self.host = self.cfg.host

        if self.cfg.host is None:
            docker_client = dockerapi.DockerApi(app_args)
            self.docker_api = docker_client.api
        else:
            self.api = model.DockerConfig(self.host, self.app_args)
            args_url = self.app_args.docker_host
            self.app_args.docker_host = self.api.url
            docker_client = dockerapi.DockerApi(self.app_args)
            self.docker_api = docker_client.api
            self.app_args.docker_host = args_url

    def build(self, nocache):
        for line in self.docker_api.build(path=self.cfg.path,
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
        sys.stdout.write("Pulling image %s:" % self.cfg.tag),
        sys.stdout.flush()
        for line in self.docker_api.pull(self.cfg.tag, stream=True):
            tick = '*'
            sys.stdout.write(tick)
            sys.stdout.flush()
        sys.stdout.write(" [done]\n")
