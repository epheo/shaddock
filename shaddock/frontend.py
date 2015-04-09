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
from shaddock import backend, model, scheduler


class Build(Command):
    """Build new container"""

    def get_parser(self, prog_name):
        parser = super(Build, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        parser.add_argument(
            '--no-cache',
            action='store_true',
            dest='no_cache',
            default='False',
            help='Build images w/o cache.'
        )
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        nocache = parsed_args.no_cache

        if name:
            if name == 'all':
                print('Building all the services...')
                schedul = scheduler.Scheduler()
                schedul.build_all(nocache,
                                  self.app_args.docker_host,
                                  self.app_args.docker_version)
            else:
                image = backend.Image(name,
                                      self.app_args.docker_host,
                                      self.app_args.docker_version)
                image.build(nocache)
        else:
            print('Please specify a name or all')

        return True


class Create(ShowOne):
    """Create new container"""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            image = backend.Image(name,
                                  self.app_args.docker_host,
                                  self.app_args.docker_version)
            image.create()
        return get_container_info(self, name, parsed_args)


class Start(ShowOne):
    """Start new container"""

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name,
                                          self.app_args.docker_host,
                                          self.app_args.docker_version)
            container.start()

        return get_container_info(self, name, parsed_args)


class Stop(ShowOne):
    """Stop container"""

    def get_parser(self, prog_name):
        parser = super(Stop, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name,
                                          self.app_args.docker_host,
                                          self.app_args.docker_version)
            container.stop()

        return get_container_info(self, name, parsed_args)


class Restart(ShowOne):
    """Restart container"""

    def get_parser(self, prog_name):
        parser = super(Restart, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name,
                                          self.app_args.docker_host,
                                          self.app_args.docker_version)
            container.restart()

        return get_container_info(self, name, parsed_args)


class Remove(ShowOne):
    """Remove container"""

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            if name == 'all':
                print('Removing all the services...')
                schedul = scheduler.Scheduler()
                schedul.remove_all(self.app_args.docker_host,
                                   self.app_args.docker_version)
            else:
                container = backend.Container(name,
                                              self.app_args.docker_host,
                                              self.app_args.docker_version)
                container.remove()
        return get_container_info(self, name, parsed_args)


class List(Lister):
    """Show a list of Containers.
       The 'Name', 'Created', 'Started', 'IP', 'Tag',
       'Docker-id' are printed by default.
    """
    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        columns = ('Name', 'Created', 'Started', 'IP', 'Tag', 'Docker-id')
        l = ()
        for svc in model.get_services_list():
            b = backend.Container(svc['name'],
                                  self.app_args.docker_host,
                                  self.app_args.docker_version)
            line = (svc['name'], b.created, b.started, b.ip, b.tag, b.id)
            l = l + (line, )
        return columns, l


class Show(ShowOne):
    "Show details about a container"

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        return get_container_info(self, name, parsed_args)


class Logs(Command):
    """Display logs of a container"""

    def get_parser(self, prog_name):
        parser = super(Logs, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        container = backend.Container(name,
                                      self.app_args.docker_host,
                                      self.app_args.docker_version)
        container.return_logs()


class Pull(Command):
    """Display logs of a container"""

    def get_parser(self, prog_name):
        parser = super(Pull, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        container = backend.Container(name,
                                      self.app_args.docker_host,
                                      self.app_args.docker_version)
        container.pull()

        return True


def get_container_info(self, name, parsed_args):
    container = backend.Container(name,
                                  self.app_args.docker_host,
                                  self.app_args.docker_version)
    columns = ('Name',
               'Created',
               'Started',
               'IP',
               'Tag',
               'Docker-id')

    data = (name,
            container.created,
            container.started,
            container.ip,
            container.tag,
            container.id)

    return columns, data
