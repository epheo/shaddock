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

import sys
import logging
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne
from panama import backend, model


class Build(Command):
    """Build new container"""

    def get_parser(self, prog_name):
        parser = super(Build, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            image = backend.Image(name)
            image.build()
        else:
            image = backend.Image('base')
            image.build()

            for i in cf.services_keys:
                image = backend.Image(i)
                image.build()
        return True


class Create(Command):

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            image = backend.Image(name)
            image.create()
            print('%s successfully created' % name)
        else:
            for i in cf.services_keys:
                image = backend.Image(i)
                image.create()
        return True


class Start(Command):

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.start()
            print('%s successfully started' % name)
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.start()
        return True


class Stop(Command):

    def get_parser(self, prog_name):
        parser = super(Stop, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.stop()
            print('%s successfully stoped' % name)
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.stop()
        return True


class Restart(Command):

    def get_parser(self, prog_name):
        parser = super(Restart, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.restart()
            print('%s successfully restarted' % name)
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.restart()
        return True


class Remove(Command):

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            container = backend.Container(name)
            container.remove()
            print('%s successfully removed' % name)
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.remove()
        return True


class List(Lister):
    """Show a list of Containers.
    The 'Name', 'Created', 'Started', 'IP', 'Tag', 'Docker-id' are printed by default.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        cf = model.ConfigFile()
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
        columns = ('Name',
                   'Created',
                   'Started',
                   'IP',
                   'Tag',
                   'Docker-id',
                   )

        b = backend.Container(name)
        data = (name,
                b.created,
                b.started,
                b.ip,
                b.tag,
                b.id)

        return columns, data
