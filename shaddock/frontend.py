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


from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne
from shaddock.drivers.docker.api import DockerApi
from shaddock.drivers.docker.container import Container
from shaddock.model import ModelDefinition
from shaddock.scheduler import Scheduler


class Create(ShowOne):
    """Create a new container"""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        schedul = Scheduler(self.app_args, parsed_args.name)
        schedul.create()
        return get_service_info(self, parsed_args)


class Start(ShowOne):
    """Start a new container"""

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        schedul = Scheduler(self.app_args, parsed_args.name)
        schedul.start()
        return get_service_info(self, parsed_args)


class Stop(ShowOne):
    """Stop a container"""

    def get_parser(self, prog_name):
        parser = super(Stop, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        schedul = Scheduler(self.app_args, parsed_args.name)
        schedul.stop()
        return get_service_info(self, parsed_args)


class Restart(ShowOne):
    """Restart a container"""

    def get_parser(self, prog_name):
        parser = super(Restart, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        schedul = Scheduler(self.app_args, parsed_args.name)
        schedul.restart()
        return get_service_info(self, parsed_args)


class Remove(ShowOne):
    """Remove a container"""

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        schedul = Scheduler(self.app_args, parsed_args.name)
        schedul.remove()
        return get_service_info(self, parsed_args)


class Build(Command):
    """Build a service"""

    def get_parser(self, prog_name):
        parser = super(Build, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        parser.add_argument(
            '--no-cache',
            action='store_true',
            dest='no_cache',
            default='False',
            help='Build images w/o cache.'
        )
        return parser

    def take_action(self, parsed_args):
        schedul = Scheduler(self.app_args, parsed_args.name)
        schedul.build()
        return True


class Pull(Command):
    """Pull a container from the Docker Repository"""

    def get_parser(self, prog_name):
        parser = super(Pull, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        schedul = Scheduler(self.app_args, parsed_args.name)
        schedul.pull()


class Logs(Command):
    """Display the logs of a container"""

    def get_parser(self, prog_name):
        parser = super(Logs, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        container = Container(name, self.app_args)
        container.return_logs()


class List(Lister):
    """Show a list of Containers.

       (epheo): imageslist is currently not returning anything as it
       refer to the list fct of dockerchecks and we would need to give
       to the DockerApi class a list of all Docker Hosts, interate on
       them and return a list of all images on all hosts.
       We should implement that on multihosts.

       Same for Container infos:
       We need to retrieve the container info list only once per host
       so split it from the container object initiation.
    """

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):

        hl = []
        model = ModelDefinition(self.app_args)
        for cluster in model.cluster_list:
            if cluster.get('hosts') is not None:
                for host in cluster.get('hosts'):
                    hl.append(host)

        # Dicts dedup (kind of set of dicts):
        #
        # The strategy is to convert the list of dictionaries to a list of
        # tuples where the tuples contain the items of the dictionary. Since
        # the tuples can be hashed, you can remove duplicates using set and,
        # after that, re-create the dictionaries from tuples with dict.
        #
        # hl is the original list
        # d is one of the dictionaries in the list
        # t is one of the tuples created from a dictionary
        hl = [{}]
        hl = [dict(t) for t in set([tuple(d.items()) for d in hl])]
        infos = []
        for host in hl:
            try:
                docker_api = DockerApi(host)
                docker_client = docker_api.connect()
                host_info = docker_client.containers(all=True)
                for info in host_info:
                    infos.append(info)
            except Exception:
                print("Failed to establish a new connection to"
                      " {} at {}.".format(host.get('name'), host.get('url')))

        columns = ('#', 'Cluster', 'Name', 'State', 'Host', 'IP', 'Image')
        l = ()
        for svc in model.get_services_list():
            svc_cfg = model.get_service(svc['name'])
            c = Container(svc['name'], svc_cfg, infos)
            host = c.cfg.get('host', 'localhost')
            ip = c.info.get('Ip')
            priority = c.cfg.get('priority', '')
            tag = c.cfg.get('image')
            cluster = c.cfg['cluster']['name']
            state = c.info.get('State')

            line = (priority, cluster, svc['name'], state, host, ip, tag)
            l = l + (line, )
        return columns, l


class Show(ShowOne):
    "Show details about a container"

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        return get_service_info(self, parsed_args)


def get_service_info(self, parsed_args):
    name = parsed_args.name
    model = ModelDefinition(self.app_args)
    data = ()
    columns = ()
    if name is None:
        for svc in model.get_services_list():
            c = Container(svc['name'], model.get_service(svc['name']))
            columns = columns + (svc['name'], )
            status = c.info.get('Status')
            data = data + (status, )
    else:
        container = Container(name, model.get_service(name))
        columns = ('Name',
                   'Created',
                   'Started',
                   'IP',
                   'Image',
                   'Docker-id')
        if container.info.get('Id') is not None:
            data = (name,
                    container.info.get('Status'),
                    container.info.get('State'),
                    container.info.get('Ip'),
                    container.cfg.get('image'),
                    container.info.get('Id'))
    return columns, data
