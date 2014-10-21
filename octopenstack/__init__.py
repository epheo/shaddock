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
import os

sys.path.insert(0, os.path.join(os.path.abspath(os.pardir)))
sys.path.insert(0, os.path.abspath(os.getcwd()))

from octopenstack import controller 
from octopenstack import view 
from octopenstack import model
from octopenstack import docker_controller

if __name__ == '__main__':

    try:
        action = sys.argv[1]
    except (TypeError, IndexError) as e:
        view.View.usage()
        exit()
        
    try:
        service    = sys.argv[2]
    except (TypeError, IndexError) as e:
        service = None

    controller = controller.Controller()

    controller.exec_service_list(action, service)
