#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import socket

class Model(object):
  
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


class ModelConstructor(object):

  def make_services_dictionary():
    services = open('../services.yaml', "r")
    yml_services = services.read()

    services_dic=yaml.load(yml_services)

    instance_name_list = services_dic.keys()

    for service in instance_name_list:
        service_info = services_dic.get(service, None)
        if service_info is not None:

            name            = service.title()
            ports           = service_info.get('ports')
            confs           = service_info.get('confs')
            volumes         = service_info.get('volumes')
            binds           = service_info.get('binds')
            privileged      = service_info.get('privileged')

            make_service(name, ports, confs, volumes, binds, privileged)

#   Glance
#   9292:9292 4324:4324
#   {'HOST_NAME': 'host_name', 'RABBITMQ_HOST': 'rabbitmq_host', 'MYSQL_USER': 'mysql_user', 'RABBITMQ_PASSWORD': 'rabbitmq_password', 'MYSQL_PASSWORD': 'mysql_pass', 'GLANCE_DBPASS': 'glance_pass', 'MYSQL_DB': 'mysql_host'}
#   {'/var/log/supervisor': '/var/log/octopenstack/glance', '/var/log/vrervefe': '/var/log/octvewacwe/fernce'}
#   None
#   False


  def make_tag(self, name):
    #      'tag': '%s/osglance' % (user), 

    return maked_tag

  def make_path(self, name):
    #      'path': '%s/glance/' % (path),

    return maked_path

  def make_ports(self, ports):
    #      'ports': [(9292, 'tcp')],

    return maked_ports

  def make_port_bindings(self, ports):
    #      'port_bindings': {9292: ('0.0.0.0', 9292)},

    return maked_port_bindings

  def make_confs(self, confs):
    #      'confs': {'HOST_NAME': host_name, 
    #                'MYSQL_DB': mysql_host, 
    #                'MYSQL_USER': mysql_user, 
    #                'MYSQL_PASSWORD': mysql_pass, 
    #                'RABBITMQ_HOST': rabbitmq_host, 
    #                'RABBITMQ_PASSWORD': rabbitmq_password, 
    #                'GLANCE_DBPASS': glance_pass
    #               },

    return maked_confs

  def make_volumes(self, volumes):
    #      'volumes': ['/var/log/supervisor'],

    return maked_volumes

  def make_binds(self, binds):
    #      'binds': {'/var/log/octopenstack/glance': {'bind': '/var/log/supervisor', 'ro': False}},

    return maked_binds

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
    print(name)
    print(ports)
    print(confs)
    print(volumes)
    print(binds)
    print(privileged)

    #return maked_service

  make_services_dictionary()