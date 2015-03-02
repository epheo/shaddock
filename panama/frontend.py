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
import argparse
from panama import backend, model


def __main__():
    parser = argparse.ArgumentParser(description='Panama provides an '
                                                 'OpenStack platform deployed '
                                                 'in Docker containers and '
                                                 'who provides and manages '
                                                 'Docker containers as cloud '
                                                 'instances.')
    parser.add_argument('-b', '--build',
                        nargs='?',
                        action='store',
                        help='Build container(s)',
                        default=False)
    parser.add_argument('-c', '--create',
                        nargs='?',
                        action='store',
                        help='Create container(s)',
                        default=False)
    parser.add_argument('-s', '--start',
                        nargs='?',
                        action='store',
                        help='Start container(s)',
                        default=False)
    parser.add_argument('--stop',
                        nargs='?',
                        action='store',
                        help='Stop container(s)',
                        default=False)
    parser.add_argument('--restart',
                        nargs='?',
                        action='store',
                        help='Restart container(s)',
                        default=False)
    parser.add_argument('-i', '--info',
                        nargs='?',
                        action='store',
                        help='Get info about container(s)',
                        default=False)
    parser.add_argument('--rm',
                        nargs='?',
                        action='store',
                        help=' container(s)',
                        default=False)
    args = vars(parser.parse_args())
    cf = model.ConfigFile()

    if args['build'] is not False:
        if args['build'] is not None:
            image = backend.Image(args['build'])
            image.build()
            print('%s successfully built' % args['build'])
        else:
            image = backend.Image('base')
            image.build()

            for i in cf.services_keys:
                image = backend.Image(i)
                image.build()

    if args['create'] is not False:
        if args['create'] is not None:
            image = backend.Image(args['create'])
            image.create()
            print('%s successfully created' % args['create'])
        else:
            for i in cf.services_keys:
                image = backend.Image(i)
                image.create()

    if args['start'] is not False:
        if args['start'] is not None:
            container = backend.Container(args['start'])
            container.start()
            print('%s successfully started' % args['start'])
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.start()

    if args['stop'] is not False:
        if args['stop'] is not None:
            container = backend.Container(args['stop'])
            container.stop()
            print('%s successfully stoped' % args['stop'])
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.stop()

    if args['restart'] is not False:
        if args['restart'] is not None:
            container = backend.Container(args['restart'])
            container.restart()
            print('%s successfully restarted' % args['restart'])
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.restart()

    if args['rm'] is not False:
        if args['rm'] is not None:
            container = backend.Container(args['rm'])
            container.remove()
            print('%s successfully removed' % args['rm'])
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.remove()

    if args['info'] is not False:
        if args['info'] is not None:
            container = backend.Container(args['info'])
            container.display_info()
        else:
            for i in cf.services_keys:
                container = backend.Container(i)
                container.display_info()

if __name__ == '__main__':
    sys.exit(__main__())