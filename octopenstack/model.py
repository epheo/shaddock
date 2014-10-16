class Model(object):
  
  import yaml
  import os
  import socket


  keystone_pass       = 'password'
  glance_pass         = 'password'
  nova_pass           = 'password'
  admin_token         = 'password'
  rabbitmq_password   = 'password'
  mysql_pass          = 'password'
  mysql_user          = 'admin'
  user                = 'octopenstack'
  path                = '%s/dockerfiles' % (os.getcwd())

  host_ip             = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
  host_name           = host_ip
  admin_password      = admin_token
  keystone_host       = host_name
  rabbitmq_host       = host_name
  mysql_host          = host_name

  services = {

      'mysql': {
          'tag': '%s/osmysql' % (user), 
          'path': '%s/mysql/' % (path),
          'ports': [(3306, 'tcp')],
          'port_bindings': {3306: ('0.0.0.0', 3306)},
          'confs': {'MYSQL_PASS': mysql_pass },
          'volumes': ['/var/log/supervisor'],
          'binds': {'/var/log/octopenstack/mysql': {'bind': '/var/log/supervisor', 'ro': False}},
          'privileged': False
          },

      'rabbitmq': {
          'tag': '%s/osrabbitmq' % (user), 
          'path': '%s/rabbitmq/' % (path),
          'ports': [(5672, 'tcp'),(15672, 'tcp')],
          'port_bindings': {5672: ('0.0.0.0', 5672), 15672: ('0.0.0.0', 15672)},
          'confs': {'RABBITMQ_PASSWORD': rabbitmq_password },
          'volumes': ['/var/log/supervisor'],
          'binds': {'/var/log/octopenstack/rabbitmq': {'bind': '/var/log/supervisor', 'ro': False}},
          'privileged': False
          },

      'glance': {
          'tag': '%s/osglance' % (user), 
          'path': '%s/glance/' % (path),
          'ports': [(9292, 'tcp')],
          'port_bindings': {9292: ('0.0.0.0', 9292)},
          'confs': {'HOST_NAME': host_name, 
                    'MYSQL_DB': mysql_host, 
                    'MYSQL_USER': mysql_user, 
                    'MYSQL_PASSWORD': mysql_pass, 
                    'RABBITMQ_HOST': rabbitmq_host, 
                    'RABBITMQ_PASSWORD': rabbitmq_password, 
                    'GLANCE_DBPASS': glance_pass
                   },
          'volumes': ['/var/log/supervisor'],
          'binds': {'/var/log/octopenstack/glance': {'bind': '/var/log/supervisor', 'ro': False}},
          'privileged': False
          },

      'horizon': {
          'tag': '%s/oshorizon' % (user), 
          'path': '%s/horizon/' % (path),
          'ports': [(80, 'tcp'),(11211, 'tcp')],
          'port_bindings': {80: ('0.0.0.0', 80), 11211: ('0.0.0.0', 11211)},
          'confs': {'HOST_NAME': host_name },
          'volumes': ['/var/log/supervisor'],
          'binds': {'/var/log/octopenstack/horizon': {'bind': '/var/log/supervisor', 'ro': False}},
          'privileged': False
          },

      'keystone': {
          'tag': '%s/oskeystone' % (user), 
          'path': '%s/keystone/' % (path),
          'ports': [(35357, 'tcp'),(5000, 'tcp')],
          'port_bindings': {35357: ('0.0.0.0', 35357), 5000: ('0.0.0.0', 5000)},
          'confs': {'HOST_NAME': host_name, 
                    'MYSQL_DB': mysql_host, 
                    'MYSQL_USER': mysql_user, 
                    'MYSQL_PASSWORD': mysql_pass, 
                    'ADMIN_TOKEN': admin_token, 
                    'KEYSTONE_DBPASS': keystone_pass
                   },
          'volumes': ['/var/log/supervisor'],
          'binds': {'/var/log/octopenstack/keystone': {'bind': '/var/log/supervisor', 'ro': False}},
          'privileged': False
          },

      'nova': {
          'tag': '%s/osnova' % (user), 
          'path': '%s/nova/' % (path),
          'ports': [(9774, 'tcp'),(8775, 'tcp')],
          'port_bindings': {8774: ('0.0.0.0', 8774), 8775: ('0.0.0.0', 8775)},
          'confs': {'HOST_NAME': host_name, 
                    'HOST_IP': host_ip, 
                    'MYSQL_DB': mysql_host, 
                    'MYSQL_USER': mysql_user, 
                    'MYSQL_PASSWORD': mysql_pass, 
                    'RABBITMQ_HOST': rabbitmq_host, 
                    'RABBITMQ_PASSWORD': rabbitmq_password, 
                    'NOVA_DBPASS': nova_pass, 
                    'ADMIN_PASS': admin_password
                   },
          'volumes': ['/var/log/supervisor'],
          'binds': {'/var/log/octopenstack/nova': {'bind': '/var/log/supervisor', 'ro': False}},
          'privileged': True
          },

#        'novacompute': {
#            'tag': '%s/osnovacompute' % (user), 
#            'path': '%s/novacompute/' % (path),
#            'confs': {'HOST_NAME': host_name },
#            'volumes': ['/var/log/supervisor'],
#            'binds': {'/var/log/octopenstack/novacompute': {'bind': '/var/log/supervisor', 'ro': False}}
#        }

#        'base': {
#            'tag': '%s/osbase' % (user), 
#            'path': '%s/base/' % (path),
#            'confs': {'HOST_NAME': host_name },
#            'volumes': ['/var/log/supervisor'],
#            'binds': {'/var/log/octopenstack/base': {'bind': '/var/log/supervisor', 'ro': False}}
#            },

  }