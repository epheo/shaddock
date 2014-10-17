#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from octopenstack import controller 

if __name__ == '__main__':
    action     = str(sys.argv[1])
    controller = controller.Controller()

    controller.exec_service_list(action)
