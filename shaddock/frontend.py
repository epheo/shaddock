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
from shaddock.openstack.common import cliutils as c


def get_container_info(name, parsed_args):
    docker_host = parsed_args.docker_host
    docker_version = parsed_args.docker_version
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

def add_arguments(parser):
    parser.add_argument(
        '--docker-host',
        action='store',
        dest='docker_host',
        default=c.env('DOCKER_HOST',
                      default='unix://var/run/docker.sock'),
        help='IP/hostname to the Docker API.  (Env: DOCKER_HOST)'
    )
    parser.add_argument(
        '--docker-version',
        action='store',
        dest='docker_version',
        default=c.env('DOCKER_VERSION',
                      default='1.12'),
        help='Docker API version number (Env: DOCKER_VERSION)'
    )

    parser.add_argument(
        '--template-dir',
        action='store',
        dest='template_dir',
        default=c.env('SHDK_TEMPLATEDIR',
                      default='/var/lib/shaddock'),
        help='Template directory to use. (Env: SHDK_TEMPLATE_DIR)'
    )
    parser.add_argument(
        '--user',
        action='store',
        dest='user',
        default=c.env('SHDK_USER',
                      default='shaddock'),
        help='User used to build Docker images. (Env: SHDK_USER)'
    )

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
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        nocache = parsed_args.no_cache
        docker_host = parsed_args.docker_host
        docker_version = parsed_args.docker_version


        if name:
            if name == 'all':
                print('Building all the services...')
                schedul = scheduler.Scheduler()
                schedul.build_all(nocache=nocache,
                                  docker_host=docker_host,
                                  docker_version=docker_version)
            else:
                image = backend.Image(name=name,
                                      docker_host=docker_host,
                                      docker_version=docker_version)
                image.build(nocache)
        else:
            print('Please specify a name or all')

        return True


class Create(ShowOne):
    """Create new container"""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        docker_host = parsed_args.docker_host
        docker_version = parsed_args.docker_version
        if name:
            image = backend.Image(name=name,
                                  docker_host=docker_host,
                                  docker_version=docker_version)
            image.create()
        return get_container_info(name, parsed_args)


class Start(ShowOne):
    """Start new container"""

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        docker_host = parsed_args.docker_host
        docker_version = parsed_args.docker_version
        if name:
            container = backend.Container(name, docker_host, docker_version)
            container.start()

        return get_container_info(name, parsed_args)


class Stop(ShowOne):
    """Stop container"""

    def get_parser(self, prog_name):
        parser = super(Stop, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        docker_host = parsed_args.docker_host
        docker_version = parsed_args.docker_version
        if name:
            container = backend.Container(name, docker_host, docker_version)
            container.stop()

        return get_container_info(name, parsed_args)


class Restart(ShowOne):
    """Restart container"""

    def get_parser(self, prog_name):
        parser = super(Restart, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        docker_host = parsed_args.docker_host
        docker_version = parsed_args.docker_version
        if name:
            container = backend.Container(name, docker_host, docker_version)
            container.restart()

        return get_container_info(name, parsed_args)


class Remove(ShowOne):
    """Remove container"""

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        docker_host = parsed_args.docker_host
        docker_version = parsed_args.docker_version
        if name:
            if name == 'all':
                print('Removing all the services...')
                schedul = scheduler.Scheduler()
                schedul.remove_all(docker_host, docker_version)
            else:
                container = backend.Container(name, docker_host, docker_version)
                container.remove()
        return get_container_info(name, parsed_args)


class List(Lister):
    """Show a list of Containers.
       The 'Name', 'Created', 'Started', 'IP', 'Tag',
       'Docker-id' are printed by default.
    """
    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        docker_host = parsed_args.docker_host
        docker_version = parsed_args.docker_version
        cf = model.Template()
        columns = ('Name', 'Created', 'Started', 'IP', 'Tag', 'Docker-id')
        l = ()
        for n in cf.services_keys:
            b = backend.Container(n, docker_host, docker_version)
            line = (n, b.created, b.started, b.ip, b.tag, b.id)
            l = l + (line, )
        return columns, l


class Show(ShowOne):
    "Show details about a container"


    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        return get_container_info(name, parsed_args)


class Logs(Command):
    """Display logs of a container"""

    def get_parser(self, prog_name):
        parser = super(Logs, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        add_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        container = backend.Container(name)
        container.return_logs()

        return True