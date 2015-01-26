#!/usr/bin/env python
# -*- coding: utf-8 -*-

from octopenstack import model
from octopenstack import view
from octopenstack import dockercontroller
#from octopenstack import init_config

class Controller(object):

    def __init__(self):
        self.model          = model.Model()
        self.view           = view.View()
        self.container      = dockercontroller.DockerController()
        #self.init_config    = init_config.InitConfig()


    def exec_service_list(self, action, service):
        if service is not None:
            self.switch(service, action)
        else:
            service_list = self.model.services.keys()
            self.view.service_list(service_list)

            result_list = []

            for service in service_list:
                
                result = self.switch(service, action)
                result_list.append(result)
	    print(result_list)
            return result_list
    
    def service_list(self):
        if service is not None:
            

    def switch(self, service, action):
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
            nocache         = self.model.nocache

            if action=='build':
                # Build base container first (cf next funct)
                self.buildbase()
                self.container.build(name, tag, path, nocache, environment)

            elif action=='run':
                id_container = self.container.create(name, tag, volumes, ports, environment)
                self.container.start(id_container, binds, port_bindings, privileged)

            elif action=='init':
                pass
                #self.init_config.mysql(name, environment)
                #self.init_config.keystone(name, environment)

            elif action=='create':
                self.container.create(name, tag, volumes, ports, environment)

            elif action=='start':
                self.container.start(id_container, binds, port_bindings)

            elif action=='stop':
                rm = False
                self.container.stop(tag, rm)

            elif action=='restart':
                rm = False
                self.container.stop(tag, rm)
                self.container.start(id_container, binds, port_bindings)
                    
            elif action=='rm':
                rm = True
                self.container.stop(tag, rm)

            elif action=='ip':
                ip = self.container.ip(tag)
                return ip

            else:
                self.view.command_not_found(action)

        else:
            self.view.service_not_found(name)

    def buildbase(self):
        name    ='osbase'
        tag     = '%s/oos-base' % (self.model.user)
        path    = '%s/base/' % (self.model.path)
        nocache = self.model.nocache
        environment = None
        self.container.build(name, tag, path, nocache, environment)
