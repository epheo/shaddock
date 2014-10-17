#!/usr/bin/env python
# -*- coding: utf-8 -*-

import docker
from octopenstack import view

docker_api = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)

class DockerController(object):

    def __init__(self):
        
        self.view = view.View()

    def build(self, name, tag, path, nocache, environment):

        action = 'building'
        quiet = False
        dockerfile = '%s/Dockerfile' % (path)
        rm = False
        stream = False
        timeout = None
        custom_context = False

        # DockerFile configuration: 
        # """""""""""""""""""""""""
        # All the parameters are include in the  services dict (here 
        # as environment).
        # They're replaced in the Dockerfile and provided to Docker as
        # a fileobj
        if not environment == None:
#            param_list = environment.keys()
#            
#            for param_key in param_list:
#                param = environment.get(param_key)

#                with open(dockerfile, "r") as dockerfile_template:
#                    template = dockerfile_template.read()

#                    print(param_key)
#                    print(param)
#                    path=None
#                    fileobj = template.replace(param_key,param)
#                    print(fileobj)
            fileobj=None
        else:
            fileobj=None
            

        self.view.service_information(action, name, tag, path, nocache)
        for line in docker_api.build(path, tag, quiet, fileobj, nocache, rm, stream, timeout, custom_context):
            self.view.display_stream(line)


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
        docker_api.start(id_container, binds, port_bindings, publish_all_ports)
        
    def get_info(self, tag):

        # Retrieve existing containers informations:
        # """"""""""""""""""""""""""""""""""""""""""
        # First  retrieve all  the instances IDs, 
        # Get informations  for  the returned IDs 
        # And check for a match with a known tag.
        #
        # Then get instances  informations in the 
        # dictionary for the matching one.
        #
        # Returned informations are stored in the 
        # 'launched_containers' dictionary.

        containers_list = docker_api.containers()

        launched_containers={}

        for containers in containers_list:
            c_id = containers.get('Id')
            container_infos = docker_api.inspect_container(c_id)

            config = container_infos.get('Config')
            if config.get('Image')==tag:
                network  = container_infos.get('NetworkSettings')

                container_specs={}
                container_specs['ipaddr']   = network.get('IPAddress')
                container_specs['dockerid'] = c_id
                container_specs['hostname'] = config.get('Hostname')

                launched_containers[tag] = container_specs

        return launched_containers

    def stop(self, tag, rm):
        launched_containers=self.get_info(tag)
        if bool(launched_containers)==True:
            containers       = launched_containers.keys()
            for container in containers:
                container_infos = launched_containers.get(container)
                dockerid = container_infos.get('dockerid')
                print('Stoping container %s ...' % (tag))
                docker_api.stop(dockerid)
                if rm==True:
                    print('Removing container %s ...' % (tag))
                    docker_api.remove_container(dockerid)
                else:
                    pass
        else:
            print('Services %s not launched' % (tag))


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