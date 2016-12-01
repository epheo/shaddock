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

import requests
from shaddock.drivers.docker.container import Container
from shaddock.model import TemplateFileError
import socket


class Checks(object):
    def __init__(self, model):
        self.model = model

    def run(self, definition):
        self.param = {}
        self.param['name'] = None
        self.param['status'] = 'running'
        self.param['host'] = None
        self.param['port'] = 80
        self.param['type'] = 'tcp'
        self.param['get'] = '/'
        self.param['code'] = 200
        self.param['state'] = 'up'
        self.param['useproxy'] = True

        # We need at least name or host
        # We Can't define name and host at the same time
        if ({'host', 'name'}.isdisjoint(set(definition.keys())) or
                {'host', 'name'}.issubset(set(definition.keys()))):
            raise TemplateFileError("Wrong check definition: "
                                    "{}".format(str(definition)))

        for opt in definition.keys():
            self.param[opt] = definition[opt]
        self.param['useproxy'] = bool(self.param['useproxy'])

        # Docker check
        if set(definition.keys()) in [{'name'}, {'name', 'status'},
                                      {'name', 'status', 'retry', 'sleep'},
                                      {'name', 'status', 'sleep'},
                                      {'name', 'status', 'retry'}]:
            return self.docker_check()

        # If tcp or http type: we need to get the ip of the corresponding
        # container. If it not available we return false (it may be just
        # starting).
        if self.param['name'] is not None:
            try:
                c = Container(self.model.get_service(self.param['name']))
                self.param['host'] = c.info.get('Ip')
                self.param['useproxy'] = False
                if c.info.get('Ip') is None:
                    return False
            except Exception:
                return False

        if self.param['type'] == 'tcp':
            return self.port_check()
        elif self.param['type'] in ['http', 'https']:
            return self.http_check()
        else:
            raise TemplateFileError("Wrong check definition: "
                                    "{}".format(str(definition)))

    def docker_check(self):
        is_up = False
        container = Container(self.model.get_service(self.param['name']))
        if 'Up' or 'running' in container.info.get('State'):
            is_up = True
        if self.param['status'] in ['running', 'up'] and is_up is True:
            return True
        if self.param['status'] in ['stopped', 'down'] and is_up is False:
            return True
        return False

    def port_check(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status = sock.connect_ex((self.param['host'], self.param['port']))
        if self.param['state'] == 'up' and status == 0:
            return True
        if self.param['state'] == 'down' and not status == 0:
            return True
        return False

    def http_check(self):
        url = (self.param['type'] + "://" + self.param['host'] +
               ":" + str(self.param['port']) + self.param['get'])
        try:
            if self.param['useproxy']:
                answ = requests.head(url, timeout=5)
            else:
                answ = requests.head(url, timeout=5,
                                     proxies={"http": "", "https": ""})
            if answ.status_code == self.param['code']:
                return True
            else:
                return False
        except Exception:
            return False
