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

import logging
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne
from shaddock import backend, model, scheduler


def get_container_info(name):
    container = backend.Container(name)
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


class Build(Command):
    """Build new container"""

    def get_parser(self, prog_name):
        parser = super(Build, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name is not None:
            if name == 'all':
                print('Here I will build all the containers for you.')
                self.scheduler.build_all()
            else:
                image = backend.Image(name)
                image.build()
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
            image = backend.Image(name)
            image.create()
        return get_container_info(name)


class Start(ShowOne):
    """Start new container"""

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.start()

        return get_container_info(name)


class Stop(ShowOne):
    """Stop container"""

    def get_parser(self, prog_name):
        parser = super(Stop, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.stop()

        return get_container_info(name)


class Restart(ShowOne):
    """Restart container"""

    def get_parser(self, prog_name):
        parser = super(Restart, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.restart()

        return get_container_info(name)


class Remove(ShowOne):
    """Remove container"""

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.remove()

        return get_container_info(name)


class List(Lister):
    """Show a list of Containers.
       The 'Name', 'Created', 'Started', 'IP', 'Tag',
       'Docker-id' are printed by default.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        cf = model.Template()
        columns = ('Name', 'Created', 'Started', 'IP', 'Tag', 'Docker-id')
        l = ()
        for n in cf.services_keys:
            b = backend.Container(n)
            line = (n, b.created, b.started, b.ip, b.tag, b.id)
            l = l + (line, )
        return columns, l


class Show(ShowOne):
    "Show details about a container"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name

        return get_container_info(name)
