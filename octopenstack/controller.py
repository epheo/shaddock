#!/usr/bin/env python
# -*- coding: utf-8 -*-

from octopenstack import model
from octopenstack import view
from octopenstack import docker_controller 

class Controller(object):

    def __init__(self):
        self.model          = model.Model()
        self.view           = view.View()
        self.container      = docker_controller.DockerController()


    def exec_service_list(self, action):
        service_list = self.model.services.keys()
        self.view.service_list(service_list)

#---------- BUILD BASE FIRST ------------#
        if action=='build':

            name    ='osbase'
            tag     = '%s/osbase' % (self.model.user)
            path    = '%s/base/' % (self.model.path)
            nocache = False
            environment = None
            self.container.build(name, tag, path, nocache, environment)

        else:
            pass

#---------- LOOP FOR EACH SERVICES ----------#
        for service in service_list:
            service_info = self.model.services.get(service, None)
            if service_info is not None:

                name            = service.title()
                tag             = service_info.get('tag')
                path            = service_info.get('path')
                ports           = service_info.get('ports')
                port_bindings   = service_info.get('port_bindings')
                environment     = service_info.get('confs')
                volumes         = service_info.get('volumes')
                binds           = service_info.get('binds')
                privileged      = service_info.get('privileged')
                nocache         = False

                if action=='build':
                    self.container.build(name, tag, path, nocache, environment)

                elif action=='run':
                    id_container = self.container.create(name, tag, volumes, ports, environment)
                    self.container.start(id_container, binds, port_bindings, privileged)

                elif action=='init':
                    self.container.create_db(name, environment)

                elif action=='create':
                    self.container.create(name, tag, volumes, ports, environment)

                elif action=='start':
                    self.container.start(id_container, binds, port_bindings)

                elif action=='stop':
                    rm = False
                    self.container.stop(tag, rm)
                        
                elif action=='rm':
                    rm = True
                    self.container.stop(tag, rm)
                else:
                    self.view.command_not_found(action)

            else:
                self.view.service_not_found(name)
