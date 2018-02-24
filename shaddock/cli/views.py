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

from shaddock.configprocessor import ConfigProcessor
from shaddock.githelper import GitHelper
from shaddock.exceptions import TemplateFileError


class Process(Command):
    """Model Config Processor
    is used to read and parse the input model and update the json db
    accordingly.
    """

    def get_parser(self, prog_name):
        parser = super(Cycle, self).get_parser(prog_name)
        parser.add_argument(
            '-a', '--append',
            action='store_true',
            dest='git_append',
            default='False',
            help='Auto append your last git commit'
        )
        parser.add_argument(
            '-m', '--model',
            action='store',
            dest='model_path',
            default='shaddock.yml',
            help='Path to model file'
        )
        parser.add_argument(
            '-d', '--dictionary',
            action='store',
            dest='dictionary_path',
            default=self.env('SHDK_DICTIONARY',
                             default='dictionary.yml'),
            help='Path to variables dictionary file'
        )
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        model_path = parsed_args.model_path
        variables_dictionary = parsed_args.variables_directory
        git_append = parsed_args.shdk_model

        git_helper = GitHelper(model_path)
        if git_append is True:
            git_helper.commit_append()
        else:
            is_commited = git_helper.check_commit_status()
            if is_commited is True:
                config_processor = ConfigProcessor(db_path, model_path,
                                                   variables_dictionary)
                config_processor.update_database()
            else:
                raise TemplateFileError(
                    "All remaining changes need to be commited before running "
                    "the config-processor, please commit your changes or add "
                    " [-a] to automatically append your last git commit."
                    )


class Cycle(Command):
    """Power-cycle a service or group of service.
    Mainly use for dev and debug purposes, it rebuild
    remove and restart a service.
    It accept a name or group_name as argument.
    """

    def get_parser(self, prog_name):
        parser = super(Cycle, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        parser.add_argument(
            '-l', '--display-logs',
            action='store_true',
            dest='with_logs',
            default='False',
            help="Display the logs of the service after the power-cycle "
                 "This option is silently ignored if a group is specified"
        )
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.cycle()

        if parsed_args.with_logs is True:
            scheduler.return_logs()


class Debug(Command):
    """Debug a container
    Open an interactive shell in a similar container
    """

    def get_parser(self, prog_name):
        parser = super(Debug, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        parser.add_argument('command', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.return_shell()


class Start(ShowOne):
    """Start a new container"""

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.start()
        return get_service_info(self, parsed_args)


class Stop(ShowOne):
    """Stop a container"""

    def get_parser(self, prog_name):
        parser = super(Stop, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.stop()
        return get_service_info(self, parsed_args)


class Restart(ShowOne):
    """Restart a container"""

    def get_parser(self, prog_name):
        parser = super(Restart, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.restart()
        return get_service_info(self, parsed_args)


class Remove(ShowOne):
    """Remove a container"""

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.remove()
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
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.build()
        return True


class Pull(Command):
    """Pull a container from the Docker Repository"""

    def get_parser(self, prog_name):
        parser = super(Pull, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.pull()


class Logs(Command):
    """Display the logs of a container"""

    def get_parser(self, prog_name):
        parser = super(Logs, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        db_path = self.app_args.db_path
        scheduler = Scheduler(db_path, parsed_args.name)
        scheduler.return_logs()


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
        parser.add_argument('name', nargs='?', default=None)

        # t is one of the tuples created from a dictionary
        hl = [{}]
        hl = [dict(t) for t in set([tuple(d.items()) for d in hl])]
        containers_all = []
        for host in hl:
            # try:
            docker_api = DockerApi(host)
            docker_client = docker_api.connect()
            containers = docker_client.containers.list(all=True)
            for c in containers:
                containers_all.append(c)
            # except Exception:
            #     print("Failed to establish a new connection to"
            #           " {} at {}.".format(host.get('name'), host.get('url')))

        columns = ('#', 'Cluster', 'Name', 'State', 'Host', 'IP', 'Image')
        lines = ()
        for svc in model.get_services_list():
            svc_cfg = model.build_service_dict(svc)
            c = Container(svc_cfg, containers_all)
            host = c.cfg.get('host', 'localhost')
            ip = c.info.get('Ip')
            priority = c.cfg.get('priority', '')
            tag = c.cfg.get('image')
            cluster = c.cfg['cluster']['name']
            state = c.info.get('State')

            line = (priority, cluster, svc['name'], state, host, ip, tag)
            lines = lines + (line, )
        return columns, lines


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
    model = ModelDefinition(self.app_args.shdk_model, self.app_args)
    data = ()
    columns = ()
    if name is None:
        for svc in model.get_services_list():
            c = Container(model.get_service(svc['name']))
            columns = columns + (svc['name'], )
            status = c.info.get('Status')
            data = data + (status, )
    else:
        container = Container(model.get_service(name))
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
