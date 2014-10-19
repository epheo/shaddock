#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from octopenstack import controller 
from octopenstack import view 

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
