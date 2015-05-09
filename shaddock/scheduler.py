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

from shaddock import model, checks
from shaddock.docker import container as dockercontainer
from shaddock.docker import image as dockerimage
from operator import itemgetter
import time


class Scheduler(object):
    def __init__(self, app_args):
        self.app_args = app_args
        self.docker_host = app_args.docker_host
        self.docker_version = app_args.docker_version
        self.services_list = model.get_services_list(self.app_args)
        self.services_list.sort(key=itemgetter('priority'))
        self.checker = checks.Checks(self.app_args)

    def build_all(self, nocache):
        for svc in self.services_list:
            image = dockerimage.Image(svc['name'], self.app_args)
            image.build(nocache)

    def create_all(self):
        for svc in self.services_list:
            container = dockercontainer.Container(svc['name'], self.app_args)
            container.create()

    def start_all(self):
        for svc in self.services_list:
            container = dockercontainer.Container(svc['name'], self.app_args)
            checks = svc.get('depends-on', [])
            if len(checks) > 0:
                print("Running checks before starting: {}".format(svc['name']))
                for check in checks:
                    self.do_check(check)
            container.start()

    def remove_all(self):
        for svc in reversed(self.services_list):
            container = dockercontainer.Container(svc['name'], self.app_args)
            container.remove()

    def pull_all(self):
        for svc in self.services_list:
            image = dockerimage.Image(svc['name'], self.app_args)
            image.pull()

    def stop_all(self):
        for svc in reversed(self.services_list):
            container = dockercontainer.Container(svc['name'], self.app_args)
            container.stop()

    def restart_all(self):
        self.stop_all()
        self.start_all()

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

