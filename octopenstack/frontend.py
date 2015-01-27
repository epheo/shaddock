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

import argparse
from octopenstack import model
from octopenstack import view
from octopenstack import backend

def __main__():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-b','--build', help='Build container(s)', default='all')
    parser.add_argument('-c','--create', help='Create container(s)', default='all')
    parser.add_argument('-s','--start', help='Start container(s)', default='all')
    parser.add_argument('-k','--kill', help='Stop (kill) container(s)', default='all')
    parser.add_argument('-i','--info', help='Get info about container(s)', default='all')
    parser.add_argument('-n','--net', help='Get IP of container(s)', default='all')
    args = vars(parser.parse_args())

    if args['build'] == 'all':
#        for i in self.model.services.get(service, None):
#            containor = backend.Container() i.title 
        pass
    elif (args.build):
        service = args['build']
        pass

    if args['create'] == 'all':
        # code here
        pass

    if args['start'] == 'all':
        # code here
        pass

    if args['kill'] == 'all':
        # code here
        pass

    if args['info'] == 'all':
        # code here
        pass

    if args['net'] == 'all':
        # code here
        pass
