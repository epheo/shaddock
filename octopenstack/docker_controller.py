#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker
from octopenstack import view

class DockerController(object):

    def __init__(self):
        docker_api = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
        self.view = view.View()

    def build(self, name, tag, path, nocache, environment):

        action = 'building'
        quiet = False
        dockerfile = '%s/Dockerfile' % (path)

        # DockerFile configuration: 
        # """""""""""""""""""""""""
        # All the parameters are include in the  services dict (here 
        # as environment).
        # They're replaced in the Dockerfile and provided to Docker as
        # a fileobj
        if not environment == None:
            param_list = environment.keys()
            
            for param_key in param_list:
                param = environment.get(param_key)

                with open(dockerfile, "r") as dockerfile_template:
                    template = dockerfile_template.read()

                    print(param_key)
                    print(param)
                    fileobj = template.replace(param_key,param)

            path=None

#        self.view.service_information(action, name, tag, path, nocache)
#        for line in docker_api.build(path, tag, quiet, fileobj, nocache):
#            print(line)


    def create(self, name, tag, volumes, ports, environment):
        action      = 'creating'
        command     = '/run.sh'
        user        = 'root'
        mem_limit   = '0'
        hostname    = name
        detach      = False
        stdin_open  = False
        tty         = False

        self.view.service_information(action, tag, command, hostname, user, ports, mem_limit, environment, volumes, name)
        id_container = docker_api.create_container(tag, command, hostname, user, detach, ports, environment, volumes, name)
        return id_container

    def start(self, id_container, binds, port_bindings, privileged):
        action            = 'starting'
        publish_all_ports = True

        self.view.service_information(action, id_container, port_bindings, privileged)
        docker_api.start(id_container, binds, port_bindings, publish_all_ports, links, privileged)
        
    def get_info(self, tag):

        # Retrieve existing containers informations:
        # """"""""""""""""""""""""""""""""""""""""""
        # First retrieve all the instances IDs, 
        # Get informations for the returned IDs 
        # And check for a match with a known tag.
        #
        # Then get instances informations in the dictionary for 
        # the matching one.
        #
        # Maybe it will be usefull to store returned information
        # in the 'services' dict?

        containers_list = docker_api.containers()

        for containers in containers_list:
            c_id = containers.get('Id')
            container_infos = docker_api.inspect_container(c_id)

            config = container_infos.get('Config')
            if config.get('Image')==tag:
                network  = container_infos.get('NetworkSettings')

                ipaddr   = network.get('IPAddress')
                dockerid = c_id
                hostname = config.get('Hostname')


    def stop(tag):
        c_id = self.get_info.dockerid(tag)
        docker_api.stop(c_id)

    def rm(tag):
        c_id = self.get_info.dockerid(tag)
        docker_api.stop(c_id)
        docker_api.remove_container(c_id)

    def create_db(self, name, environment):
#        import MySQLdb

        print(environment)

#        db = MySQLdb.connect(host,user,passwd,db)
#        cur = db.cursor() 

#        cur.execute("CREATE DATABASE %s;" % (name))
#        cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'localhost' IDENTIFIED BY '${GLANCE_DBPASS}';")
#        cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'${HOST_NAME}' IDENTIFIED BY '${GLANCE_DBPASS}';")
#        cur.execute("GRANT ALL PRIVILEGES ON ${SERVICE}.* TO '${SERVICE}'@'%' IDENTIFIED BY '${GLANCE_DBPASS}'")

#    def config_files():