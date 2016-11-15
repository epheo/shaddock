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

from operator import itemgetter
from shaddock import checks
from shaddock.drivers.docker import container as dockercontainer
from shaddock.drivers.docker import image as dockerimage
from shaddock.model import ModelDefinition
from shaddock.model import TemplateFileError
import time


class Scheduler(object):
    def __init__(self, app_args):
        self.app_args = app_args
        self.docker_host = app_args.docker_host
        self.docker_version = app_args.docker_version
        model = ModelDefinition(self.app_args)
        self.services_list = model.get_services_list()
        try:
            self.services_list.sort(key=itemgetter('priority'))
        except KeyError:
            raise TemplateFileError(
                "In order to use the scheduler functionality, all the "
                "services from your model need to have the priority "
                "argument defined. At least one of your services does "
                "not have this argument set.")
            
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


class CheckError(Exception):
        pass
