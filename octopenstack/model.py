#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import socket

class Model(object):

  def make_services_dictionary(self):
    services = open('../services.yaml', "r")
    yml_services = services.read()

    services_dic=yaml.load(yml_services)

    instance_name_list = services_dic.keys()

    configuration = open('../configuration.yaml', "r")
    yml_config    = configuration.read()
    config_dic    = yaml.load(yml_config)
    confs         = config_dic.get('confs')

    for service in instance_name_list:
        service_info = services_dic.get(service, None)
        if service_info is not None:

            name            = service.title()
            ports           = service_info.get('ports')
            volumes         = service_info.get('volumes')
            binds           = service_info.get('binds')
            privileged      = service_info.get('privileged')

            self.make_service(name, ports, confs, volumes, binds, privileged)


    print(config_dic)

#   Glance
#   9292:9292 4324:4324
#   {'HOST_NAME': 'host_name', 'RABBITMQ_HOST': 'rabbitmq_host', 'MYSQL_USER': 'mysql_user', 'RABBITMQ_PASSWORD': 'rabbitmq_password', 'MYSQL_PASSWORD': 'mysql_pass', 'GLANCE_DBPASS': 'glance_pass', 'MYSQL_DB': 'mysql_host'}
#   {'/var/log/supervisor': '/var/log/octopenstack/glance', '/var/log/vrervefe': '/var/log/octvewacwe/fernce'}
#   None
#   False


  def make_service(self, name, ports, confs, volumes, binds, privileged):
    #  'glance': {
    #      'tag': '%s/osglance' % (user), 
    #      'path': '%s/glance/' % (path),
    #      'ports': [(9292, 'tcp')],
    #      'port_bindings': {9292: ('0.0.0.0', 9292)},
    #      'confs': {'HOST_NAME': host_name, 
    #                'MYSQL_DB': mysql_host, 
    #                'MYSQL_USER': mysql_user, 
    #                'MYSQL_PASSWORD': mysql_pass, 
    #                'RABBITMQ_HOST': rabbitmq_host, 
    #                'RABBITMQ_PASSWORD': rabbitmq_password, 
    #                'GLANCE_DBPASS': glance_pass
    #               },
    #      'volumes': ['/var/log/supervisor'],
    #      'binds': {'/var/log/octopenstack/glance': {'bind': '/var/log/supervisor', 'ro': False}},
    #      'privileged': False
    #      },
    #print(name, ports, confs, volumes, binds, privileged)

    keystone_pass       = 'password'
    glance_pass         = 'password'
    nova_pass           = 'password'
    admin_token         = 'password'
    rabbitmq_password   = 'password'
    mysql_pass          = 'password'
    mysql_user          = 'admin'
    user                = 'octopenstack'

    path                = '%s/dockerfiles' % (os.getcwd())
    #host_ip             = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    host_ip             = '192.168.3.200'
    host_name           = host_ip
    admin_password      = admin_token
    keystone_host       = host_name
    rabbitmq_host       = host_name
    mysql_host          = host_name

    service_dic = {}

    ## Register Tag
    service_dic['tag'] = '%s/oos-%s' % (user, name)

    ## Register Path
    service_dic['path'] = '%s/%s' % (path, name)

    ## Register Ports
    ports_list=[]
    for port in ports:
      ports_list.append((port, 'tcp'))
    service_dic['ports'] = ports_list

    ## Register port_bindings
    for port in ports:
      service_dic['ports'] = {port: ('0.0.0.0', port)}

    ## Register confs
    #service_dic['confs'] = ??

    ## Register volumes and binds

    ports_list=[]
    for port in ports:
      ports_list.append((port, 'tcp'))
    service_dic['ports'] = ports_list

    volumes_list=[]
    binds_dico={}
    for volume in volumes.keys():
      volumes_list.append(volume)
      bind = volumes.get(volume)
      binds_dico[bind] = {'bind': volume, 'ro': False}

    service_dic['volumes'] = volumes_list
    service_dic['binds'] = binds_dico

    #TEST
    print(service_dic)

    #return maked_service

if __name__ == '__main__':
  model=Model()
  model.make_services_dictionary()