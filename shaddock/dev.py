from jinja2 import Environment
from jinja2 import FileSystemLoader
import os.path
from shaddock.exceptions import TemplateFileError
from tinydictdb import TinyDictDb
import yaml
import pprint


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


# Tests

y = {'key1': 'value_y',
     'key2': ['value2', 'value3', 'value6'],
     'key3': 'value1',
     }

z = {'key1': 'value_z',
     'key2': ['value7', 'value3', 'value1'],
     'key3': 'value1',
     }

expected_stage1 = {
    'groups': [
        {
            'name': 'group-1',
            'key_bool': True,
            'key_list': ['value-0', 'value-1', 'value-2'],
            'objects': ['obj-1', 'obj-2'],
            'groups': ['group-2'],
        },
        {
            'name': 'group-2',
            'key_bool': False,
            'key_list': ['value-3', 'value-1', 'value-2'],
            'objects': ['obj-3', 'obj-2'],
        },
    ],
    'objects': [
        {
            'name': 'obj-1',
            'key_list': ['value-3-2', 'value-1', 'value-2'],
            'key_bool': False,
            'key_str': '1',
        },
        {
            'name': 'obj-2',
            'key_list': ['value-3-3', 'value-1', 'value-2'],
            'key_str': '2',
        },
        {
            'name': 'obj-3',
            'key_list': ['value-3-3', 'value-1', 'value-2'],
            'key_bool': True,
            'key_str': '3',
        },
    ],
}

expected_stage2 = {
    'groups': [
        {
            'name': 'group-1',
            'key_bool': True,
            'key_list': ['value-0', 'value-1', 'value-2'],
            'objects': ['obj-1', 'obj-2'],
        },
        {
            'name': 'group-2',
            'key_bool': False,
            'key_list': ['value-0', 'value-3', 'value-1', 'value-2'],
            'objects': ['obj-3', 'obj-2'],
        }
    ],
    'objects': [
        {
            'name': 'obj-1',
            'key_list': ['value-0', 'value-3-2', 'value-1', 'value-2'],
            'key_str': '1',
        },
        {
            'name': 'obj-2',
            'key_list': ['value-0', 'value-3-3', 'value-3', 'value-1'],
            'key_str': '2',
        },
        {
            'name': 'obj-3',
            'key_list': ['value-0', 'value-3', 'value-3-3', 'value-1'],
            'key_bool': True,
            'key_str': '3',
        }
    ],
}

expected_stage3 = [
    {
        'name': 'obj-1',
        'key_list': ['value-3-2', 'value-1', 'value-2'],
        'key_bool': False,
        'key_str': '1',
    },
    {
        'name': 'obj-2',
        'key_list': ['value-3-3', 'value-1', 'value-2'],
        'key_str': '2',
    },
    {
        'name': 'obj-3',
        'key_list': ['value-3-3', 'value-1', 'value-2'],
        'key_bool': True,
        'key_str': '3',
    },
]

pp = pprint.PrettyPrinter(indent=4)

model = merge_similar_keys(y, z)
# pp.pprint(model)

objects_key = 'objects'
groups_key = 'groups'
model_2 = stage2(expected_stage1, objects_key, groups_key)
# pp.pprint(model_2)

objects_key = 'objects'
groups_key = 'groups'
model_3 = stage3(expected_stage2, objects_key, groups_key)
# pp.pprint(model_3)

vardict = 'tests/v2/dictionary.yml'
model = 'tests/v2/'
model_1 = stage1(vardict, model)
# pp.pprint(model)

objects_key = 'services'
groups_key = 'service-groups'
model_2 = stage2(model_1, objects_key, groups_key)
# pp.pprint(model_2)

model_3 = stage3(model_2, objects_key, groups_key)
pp.pprint(model_3)
