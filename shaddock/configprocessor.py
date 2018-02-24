#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from jinja2 import Template
from jinja2 import FileSystemLoader
import os.path
import yaml
from tinydictdb import TinyDictDb


class ConfigProcessor(object):
    """ Input Model processor

    This class parse and process the input model and populate the
    json database accordingly.
    """

    def __init__(self, model_path, vardict, db_path):
        self.db = TinyDictDb(path=db_path)
        self.vardict = vardict
        self.model = model_path

    def _render(self):
        with open(vardict, 'r') as stream:
            context = yaml.load(stream)
            print(context)
        env = Environment(loader=FileSystemLoader(self.model))
        if os.path.isfile(self.model):
            return env.get_template(self.model).render(context)
        else:

            for f in os.listdir(self.model):
                z = {**x, **y}
                env.get_template(f).render(context)

    def _get_service_groups(self):
        pass

    def _get_hosts_groups(self):
        pass

    def _inherit_from_group(self):
        pass

    def update_hosts(self):
        pass

    def update_networks(self):
        pass

    def update_vports(self):
        pass

    def update_services(self):
        pass

    def update_database_from_model(self):
        pass

class Loader(yaml.Loader):
    """Include

    This class change the Yaml Load fct to allow file inclusion
    using the !include keywork.
    """
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)


    def import_str(self, node):
        return str(self.construct_scalar(node))
