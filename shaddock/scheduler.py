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

from shaddock import model, backend


class Scheduler(object):
    def __init__(self):
        services_dict = model.get_services_dict()
        self.names_list = []
        for service in services_dict.keys():
            self.names_list.append(service.lower())

    def build_all(self, nocache, docker_host, docker_version):
        for name in self.names_list:
            image = backend.Image(name, docker_host, docker_version)
            image.build(nocache)

    def remove_all(self, docker_host, docker_version):
        for name in self.names_list:
            container = backend.Container(name, docker_host, docker_version)
            container.remove()

    def order_by_priority(self):
        raise NotImplementedError

    def wait(self):
        raise NotImplementedError


class Checks(object):
    def __init__(self, container):
        raise NotImplementedError

    def tcp_check(self):
        raise NotImplementedError

    def http_check(self):
        raise NotImplementedError

    def docker_check(self):
        raise NotImplementedError

