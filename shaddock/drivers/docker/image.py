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
from shaddock.drivers.docker.api import DockerApi
import sys


class Image(object):

    def __init__(self, name, model, infos=None):
        self.name = name
        self.cfg = model.get_service(self.name)
        docker_api = DockerApi(self.cfg['api_cfg'])
        self.docker_client = docker_api.connect()

    def build(self, nocache=None):
        for line in self.docker_client.build(
            path=self.cfg['path'],
            tag=self.cfg['image'],
            quiet=False,
            fileobj=None,
            nocache=nocache,
            rm=False,
            stream=False,
            timeout=None,
            custom_context=False,
            encoding=None,
            pull=False,
            forcerm=False,
            dockerfile=None,
            container_limits=None,
            decode=False,
            buildargs=None,
            gzip=False,
            # shmsize=None,
            # labels=None
            ):

            try:
                jsonstream = json.loads(line.decode())
            except UnicodeDecodeError:
                pass
            stream = jsonstream.get('stream')
            error = jsonstream.get('error')
            if error is not None:
                print(error.rstrip())
            if stream is not None:
                print(stream.rstrip())

    def pull(self):
        sys.stdout.write("Pulling image %s:" % self.cfg['tag']),
        sys.stdout.flush()
        for line in self.docker_client.pull(self.cfg['image'], stream=True):
            tick = '*'
            sys.stdout.write(tick)
            sys.stdout.flush()
        sys.stdout.write(" [done]\n")
