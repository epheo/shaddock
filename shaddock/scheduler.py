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
from operator import itemgetter
import time
import docker
import socket
import requests


class Scheduler(object):
    def __init__(self):
        self.services_list = model.get_services_list()
        self.services_list.sort(key=itemgetter('priority'))
        self.checker = Checks()

    def build_all(self, nocache, docker_host, docker_version):
        for svc in self.services_list:
            image = backend.Image(svc['name'], docker_host, docker_version)
            image.build(nocache)

    def create_all(self, docker_host, docker_version):
        for svc in self.services_list:
            container = backend.Container(svc['name'], docker_host,
                                          docker_version)
            container.create()

    def start_all(self, docker_host, docker_version):
        for svc in self.services_list:
            container = backend.Container(svc['name'], docker_host,
                                          docker_version)
            checks = svc.get('depends-on', [])
            if len(checks) > 0:
                print("Running checks before starting: {}".format(svc['name']))
                for check in checks:
                    self.do_check(check)
            container.start()

    def remove_all(self, docker_host, docker_version):
        for svc in reversed(self.services_list):
            container = backend.Container(svc['name'], docker_host,
                                          docker_version)
            container.remove()

    def pull_all(self, docker_host, docker_version):
        for svc in self.services_list:
            image = backend.Image(svc['name'], docker_host, docker_version)
            image.pull()

    def stop_all(self, docker_host, docker_version):
        for svc in reversed(self.services_list):
            container = backend.Container(svc['name'], docker_host,
                                          docker_version)
            container.stop()

    def restart_all(self, docker_host, docker_version):
        self.stop_all(docker_host, docker_version)
        self.start_all(docker_host, docker_version)

    def do_check(self, check, retry=None):
        if retry is None:
            retry = check.get('retry', 15)
        elif retry == 0:
            raise CheckError("The following check ran it's maximum amount of"
                             " retry and is still returning "
                             " False:".format(str(check)))
        print("Running check: {}".format(str(check)))
        if self.checker.run(check):
            pass
        else:
            retry -= 1
            time.sleep(check.get('sleep', 10))
            self.do_check(check, retry)


class Checks(object):
    def __init__(self, d_ver='1.12', d_host='unix:///var/run/docker.sock'):
        self.dockerapi = docker.Client(base_url=d_host,
                                       version=str(d_ver),
                                       timeout=10)
        self.d_ver = d_ver
        self.d_host = d_host

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
            raise model.TemplateFileError("Wrong check definition: "
                                          "{}".format(str(definition)))

        for opt in definition.keys():
            self.param[opt] = definition[opt]
        self.param['useproxy'] = bool(self.param['useproxy'])

        # Docker check
        if set(definition.keys()) in [{'name'}, {'name', 'status'}]:
            return self.docker_check()

        # If tcp or http type: we need to get the ip of the corresponding
        # container. If it not available we return false (maybe it is just
        # starting).
        if self.param['name'] is not None:
            try:
                c = backend.Container(self.param['name'], self.d_host,
                                      self.d_ver)
                self.param['host'] = c.ip
                self.param['useproxy'] = False
                if c.ip is None:
                    return False
            except:
                return False

        if self.param['type'] == 'tcp':
            return self.port_check()
        elif self.param['type'] in ['http', 'https']:
            return self.http_check()
        else:
            raise model.TemplateFileError("Wrong check definition: "
                                          "{}".format(str(definition)))

    def docker_check(self):
        try:
            status = [c['Status'][:2].lower()
                      for c in self.dockerapi.containers()
                      if (c['Names'][0][1:] == self.param['name'])][0]
        except IndexError:
            status = 'down'
        if self.param['status'] in ['running', 'up']:
            if status == 'up':
                ret = True
            else:
                ret = False
        elif self.param['status'] in ['stopped', 'down']:
            if status == 'up':
                ret = False
            else:
                ret = True
        return ret

    def port_check(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status = sock.connect_ex((self.param['host'], self.param['port']))
        if self.param['state'] == 'up':
            if status == 0:
                ret = True
            else:
                ret = False
        elif self.param['state'] == 'down':
            if status == 0:
                ret = False
            else:
                ret = True
        return ret

    def http_check(self):
        url = (self.param['type'] + "://" + self.param['host'] +
               ":" + str(self.param['port']) + self.param['get'])
        print(url)
        try:
            if self.param['useproxy']:
                answ = requests.head(url, timeout=5)
            else:
                answ = requests.head(url, timeout=5,
                                     proxies={"http": "", "https": ""})
            if answ.status_code == self.param['code']:
                ret = True
            else:
                ret = False
        except:
            ret = False
        return ret


class CheckError(Exception):
        pass
