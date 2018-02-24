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
from shaddock.checks import Checks
from shaddock.drivers.docker.container import Container
from shaddock.drivers.docker.image import Image
from shaddock.model import ModelDefinition
from shaddock.exceptions import TemplateFileError
from shaddock.exceptions import CheckError
import time


class Scheduler(object):

    def __init__(self, db_path, name):
        # Define if name is a :
        # - group name
        # - servive name
        # - list of service names
        # - list of groups
        # And self a list of services anyway
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
            self.checker = Checks(self.model)

    def build(self):
        if self.name is None:
            for svc in self.services_list:
                image = Image(self.model.build_service_dict(svc))
                image.build()
        else:
            image = Image(self.model.get_service(self.name))
            image.build()

    def create(self):
        if self.name is None:
            for svc in self.services_list:
                container = Container(self.model.build_service_dict(svc))
                try:
                    container.create()
                except Exception:
                    pass
        else:
            container = Container(self.model.get_service(self.name))
            container.create()

    def cycle(self):
        if self.name is None:
            for svc in reversed(self.services_list):
                container = Container(self.model.build_service_dict(svc))
                image = Image(self.model.build_service_dict(svc))
                image.build()
                container.remove()
                container.start()
        else:
            image = Image(self.model.get_service(self.name))
            container = Container(self.model.get_service(self.name))
            image.build()
            container.remove()
            container.start()

    def start(self):
        if self.name is None:
            for svc in self.services_list:
                container = Container(self.model.build_service_dict(svc))
                checks = svc.get('depends-on', [])
                if len(checks) > 0:
                    print("Running checks before "
                          "starting: {}".format(svc['name']))
                    for check in checks:
                        self.do_check(check)
                container.start()
        else:
            container = Container(self.model.get_service(self.name))
            container.start()

    def remove(self):
        if self.name is None:
            for svc in reversed(self.services_list):
                container = Container(self.model.build_service_dict(svc))
                container.remove()
        else:
            container = Container(self.model.get_service(self.name))
            container.remove()

    def pull(self):
        if self.name is None:
            for svc in self.services_list:
                image = Image(self.model.build_service_dict(svc))
                image.pull()
        else:
            image = Image(self.model.get_service(self.name))
            image.pull()

    def stop(self):
        if self.name is None:
            for svc in reversed(self.services_list):
                container = Container(self.model.build_service_dict(svc))
                container.stop()
        else:
            container = Container(self.model.get_service(self.name))
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

