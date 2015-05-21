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

def check(app_args, param):

    docker_host = app_args.docker_host
    docker_version = app_args.docker_version
    docker_api = docker.Client(base_url=docker_host,
                               version=docker_version,
                               timeout=10)

    try:
        status = [c['Status'][:2].lower()
                  for c in docker_api.containers()
                  if (c['Names'][0][1:] == param['name'])][0]
    except IndexError:
        status = 'down'
    if param['status'] in ['running', 'up']:
        if status == 'up':
            ret = True
        else:
            ret = False
    elif param['status'] in ['stopped', 'down']:
        if status == 'up':
            ret = False
        else:
            ret = True
    return ret

def list(app_args):
    docker_host = app_args.docker_host
    docker_version = app_args.docker_version
    docker_api = docker.Client(base_url=docker_host,
                               version=docker_version,
                               timeout=10)

    return docker_api.images()
