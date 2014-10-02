#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from fabric.api import *
import docker
import os

class Model(object):
    path = os.getcwd()
    user = 'epheo'

    services = {
        'base': {'tag': '%s/osbase' % (user), 'path': '%s/base/' % (path)},
        'mysql': {'tag': '%s/osmysql' % (user), 'path': '%s/mysql/' % (path)},
        'rabbitmq': {'tag': '%s/osrabbitmq' % (user), 'path': '%s/base/' % (path)}
    }

class View(object):

    def service_list(self, service_list):
        print('service LIST:')
        for service in service_list:
            print(service)
        print('')

    def service_information(self, service, service_info):
        print('service INFORMATION:')
        print('Name: %s, Tag: %s, Path: %s\n' % (service.title(), 
                                                     service_info.get('tag', 0), 
                                                     service_info.get('path', 0)
                                                    )
             )

    def service_build_status(self, buildstatus):
        for line in buildstatus:
            print(line)

    def service_not_found(self, service):
        print('That service "%s" does not exist' % service)


class Controller(object):

    def __init__(self):
        self.model = Model()
        self.view = View()

    def get_service_list(self):
        service_list = self.model.services.keys()
        self.view.service_list(service_list)

    def build_service(self, service):
        service_info = self.model.services.get(service, None)
        if service_info is not None:
            self.view.service_information(service, service_info, buildstatus)
            buildstatus = docker_api.build(path = service_info.get('path', 0), tag = service_info.get('tag', 0))
            self.view.service_build_status(buildstatus)
        else:
            self.view.service_not_found(service)


if __name__ == '__main__':
    docker_api = docker.Client(base_url='unix://var/run/docker.sock',
                               version='1.12',
                               timeout=10)

    controller = Controller()
    controller.get_service_list()
    controller.build_service('base')
    controller.build_service('mysql')
    controller.build_service('rabbitmq')
    controller.build_service('arepas')
