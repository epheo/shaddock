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

from jinja2 import Environment
from jinja2 import FileSystemLoader
from os import path
from shaddock.exceptions import TemplateFileError
from tinydictdb import TinyDictDb
import yaml

class ConfigProcessor(object):

    vardict = 'tests/v2/dictionary.yml'
    model = 'tests/v2/'
    
    def update_database(self, db, dictionary, model):
        db = path.join(db, object_key)
        db = TinyDictDb(path=db, wMode='append')
        services = self.parse_services(self.vardict, model)
        db.addEntries(services)
    
    def parse_hosts(self, vardict, model):
        model_1 = self.stage1(vardict, model)
        objects_key = 'hosts'
        groups_key = 'host-groups'
        model_2 = self.stage2(model_1, objects_key, groups_key)
        model_3 = self.stage3(model_2, objects_key, groups_key)
        return model_3
    
    def parse_networks(self, vardict, model):
        model_1 = self.stage1(vardict, model)
        objects_key = 'ports'
        groups_key = 'networks'
        model_2 = self.stage2(model_1, objects_key, groups_key)
        model_3 = self.stage3(model_2, objects_key, groups_key)
        return model_3
    
    def parse_vports(self, vardict, model):
        model_1 = self.stage1(vardict, model)
        objects_key = 'ports'
        groups_key = 'networks'
        model_2 = self.stage2(model_1, objects_key, groups_key)
        model_3 = self.stage3(model_2, objects_key, groups_key)
        return model_3
    
    def parse_services(self, vardict, model):
        model_1 = self.stage1(vardict, model)
        objects_key = 'services'
        groups_key = 'service-groups'
        model_2 = stage2(model_1, objects_key, groups_key)
        model_3 = stage3(model_2, objects_key, groups_key)
        return model_3
    
def merge_similar_keys(y, z):
    """ y and z are two dictionaries

    if value is a list, y and z are merged
    if value is a string, z take precedence
    """

    for k, v in y.items():
        if k in z:
            if type(v) == list:
                p = [v, z[k]]
                flat = [i for s in p for i in s]
                z[k] = flat
        else:
            z[k] = v
    return z


def get_by_name(name, dict_list):
    """ Return the element with a matching name from
    a list of dictionaries
    """
    for d in dict_list:
        if d.get('name') == name:
            return d


def stage1(vardict, model):
    """ Stage 1

    - read all files
    - jinja2 templating
    - merge of all similar keys into a single dictionary
    """

    with open(vardict, 'r') as stream:
        context = yaml.load(stream)
    env = Environment(loader=FileSystemLoader(model))

    z = {}
    for f in os.listdir(model):
        y = yaml.load(env.get_template(f).render(context))
        if y:
            merge_similar_keys(y, z)
    return z


def stage2(m, objects_key, groups_key):
    """ Stage 2

    group inheritance

    current issues:
    - only one inheritence level
    """

    group_list = []
    for group in m.get(groups_key):
        if group is None:
            return m
        if group.get(groups_key):
            res = group.copy()
            res.pop(groups_key)
            group_list.append(res)
            for child in group.get(groups_key):
                group.pop(groups_key)
                group.pop(objects_key)
                child = get_by_name(child, m.get(groups_key))
                res = merge_similar_keys(group, child)
                group_list.append(res)
    m.pop(groups_key)
    m[groups_key] = group_list
    return m


def stage3(m, objects_key, groups_key):
    """ Stage 3

    object inheritance
    """

    object_list = []
    for g in m.get(groups_key):
        if g is None:
            return m
        for obj_name in g.get(objects_key):
            for o in m.get(objects_key):
                if o.get('name') == obj_name:
                    obj_result = merge_similar_keys(g, o)
                    try:
                        obj_result.pop(objects_key)
                    except KeyError:
                        pass
                    object_list.append(obj_result)
    return object_list

