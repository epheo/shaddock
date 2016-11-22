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
from shaddock.drivers.docker.container import Container
from shaddock.drivers.docker.image import Image
from shaddock.model import ModelDefinition
from shaddock.model import TemplateFileError
import time


class Scheduler(object):
    def __init__(self, app_args, name=None):
        self.model = ModelDefinition(app_args)
        self.services_list = self.model.get_services_list()
        self.name = name
        if name is None:
            try:
                self.services_list.sort(key=itemgetter('priority'))
            except KeyError:
                raise TemplateFileError(
                    "In order to use the scheduler functionality, all the "
                    "services from your model needs to have the priority "
                    "argument defined. At least one of your services does "
                    "not have this argument set.")
            self.checker = checks.Checks(app_args)

    def build(self):
        if self.name is None:
            for svc in self.services_list:
                image = Image(svc['name'])
                image.build()
        else:
            image = Image(self.name)
            image.build()

    def create(self):
        if self.name is None:
            for svc in self.services_list:
                svc_cfg = self.model.get_service(svc['name'])
                container = Container(svc['name'], svc_cfg)
                try:
                    container.create()
                except Exception:
                    pass
        else:
            svc_cfg = self.model.get_service(self.name)
            container = Container(self.name, svc_cfg)
            container.create()

    def start(self):
        if self.name is None:
            for svc in self.services_list:
                svc_cfg = self.model.get_service(svc['name'])
                container = Container(svc['name'], svc_cfg)
                checks = svc.get('depends-on', [])
                if len(checks) > 0:
                    print("Running checks before "
                          "starting: {}".format(svc['name']))
                    for check in checks:
                        self.do_check(check)
                container.start()
        else:
            container = Container(self.name,
                                  self.model.get_service(self.name))
            container.start()

    def remove(self):
        if self.name is None:
            for svc in reversed(self.services_list):
                svc_cfg = self.model.get_service(svc['name'])
                print(svc_cfg)
                container = Container(svc['name'], svc_cfg)
                container.remove()
        else:
            svc_cfg = self.model.get_service(self.name)
            container = Container(self.name, svc_cfg)
            container.remove()

    def pull(self):
        if self.name is None:
            for svc in self.services_list:
                image = Image(svc['name'])
                image.pull()
        else:
            image = Image(self.name)
            image.pull()

    def stop(self):
        if self.name is None:
            for svc in reversed(self.services_list):
                self.model.get_service(svc['name'])
                container = Container(svc['name'],
                                      self.model.get_service(svc['name']))
                container.stop()
        else:
            container = Container(self.name,
                                  self.model.get_service(self.name))
            container.stop()

    def restart(self):
        self.stop()
        self.start()

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
