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
from shaddock.drivers.docker import container as dockercontainer
from shaddock.drivers.docker import image as dockerimage
from shaddock.model import ModelDefinition
from shaddock import scheduler


class Build(Command):
    """Build a new container"""

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
                print('Building all services...')
                schedul = scheduler.Scheduler(self.app_args)
                schedul.build_all(nocache)
            else:
                image = dockerimage.Image(name,
                                          self.app_args)
                image.build(nocache)
        else:
            raise IndexError
        return True


class Create(ShowOne):
    """Create a new container"""

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            if name == 'all':
                print('Creating all containers...')
                schedul = scheduler.Scheduler(self.app_args)
                schedul.create_all()
            else:
                container = dockercontainer.Container(name,
                                                      self.app_args)
                container.create()
        else:
            raise IndexError
        return get_container_info(self, name, parsed_args)


class Start(ShowOne):
    """Start a new container"""

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            if name == 'all':
                print('Starting all containers...')
                schedul = scheduler.Scheduler(self.app_args)
                schedul.start_all()
            else:
                container = dockercontainer.Container(name,
                                                      self.app_args)
                container.start()
        else:
            raise IndexError
        return get_container_info(self, name, parsed_args)


class Stop(ShowOne):
    """Stop a container"""

    def get_parser(self, prog_name):
        parser = super(Stop, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            if name == 'all':
                print('Stopping all containers...')
                schedul = scheduler.Scheduler(self.app_args)
                schedul.stop_all()
            else:
                container = dockercontainer.Container(name,
                                                      self.app_args)
                container.stop()
        else:
            raise IndexError
        return get_container_info(self, name, parsed_args)


class Restart(ShowOne):
    """Restart a container"""

    def get_parser(self, prog_name):
        parser = super(Restart, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            if name == 'all':
                print('Restarting all containers...')
                schedul = scheduler.Scheduler(self.app_args)
                schedul.restart_all()
            else:
                container = dockercontainer.Container(name,
                                                      self.app_args)
                container.restart()
        else:
            raise IndexError
        return get_container_info(self, name, parsed_args)


class Remove(ShowOne):
    """Remove a container"""

    def get_parser(self, prog_name):
        parser = super(Remove, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            if name == 'all':
                print('Removing all containers...')
                schedul = scheduler.Scheduler(self.app_args)
                schedul.remove_all()
            else:
                container = dockercontainer.Container(name,
                                                      self.app_args)
                container.remove()
        else:
            raise IndexError
        return get_container_info(self, name, parsed_args)


class List(Lister):
    """Show a list of Containers.

       The 'Name', 'Created', 'Started', 'IP', 'Tag',
       'Docker-id' are printed by default.

       (epheo): imageslist is currently not returning anything as it
       refer to the list fct of dockerchecks and we would need to give
       to the DockerApi class a list of all Docker Hosts, interate on
       them and return a list of all images on all hosts.
       This is currently not implemented on multihosts
    """

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        columns = ('Name', 'Status', 'Host', 'IP', 'Image')
        # imageslist = dockerchecks.list(self.app_args)

        l = ()
        model = ModelDefinition(self.app_args)

        for svc in model.get_services_list():
            b = dockercontainer.Container(svc['name'],
                                          self.app_args)
            """Return the container id, but not used for now.

            if b.id:
                container_id = b.id[:12]
            else:
                container_id = b.id

            # Return the image build state, but not used for now.

            try:
                img_build = [img['Created'] for img in imageslist
                             if b.tag in img['RepoTags']][0]
                img_build = time.strftime('%m/%d %H:%M',
                                          time.localtime(img_build))
            except Exception:
                img_build = None
            """

            if 'host' in svc:
                host = svc['host']
            else:
                host = 'localhost'

            line = (svc['name'], b.status, host, b.ip, b.tag)
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
    """Display the logs of a container"""

    def get_parser(self, prog_name):
        parser = super(Logs, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        container = dockercontainer.Container(name, self.app_args)
        container.return_logs()


class Pull(Command):
    """Pull a container from the Docker Repository"""

    def get_parser(self, prog_name):
        parser = super(Pull, self).get_parser(prog_name)
        parser.add_argument('name', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        if name:
            if name == 'all':
                print('Pulling all containers...')
                schedul = scheduler.Scheduler(self.app_args)
                schedul.pull_all()

            else:
                image = dockerimage.Image(name, self.app_args)
                image.pull()
        else:
            raise IndexError


def get_container_info(self, name, parsed_args):
    if name == 'all':
        columns = ('Name',)
        data = (name,)
    else:
        container = dockercontainer.Container(name, self.app_args)
        columns = ('Name',
                   'Created',
                   'Started',
                   'IP',
                   'Image',
                   'Docker-id')
        if container.id:
            c_id = container.id[:12]
        else:
            c_id = None
        data = (name,
                container.created,
                container.started,
                container.ip,
                container.tag,
                c_id)
    return columns, data
