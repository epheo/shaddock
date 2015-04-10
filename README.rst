**Shaddock**
============
Shaddock provides a platform deployed in http://docker.com containers following
a predefined template (like an http://openstack.org infrastructure)

QuickStart
----------

.. code:: bash

    git clone https://github.com/epheo/shaddock
    git clone https://github.com/epheo/shaddock-openstack /var/lib/shaddock/
    cd shaddock && sudo python setupy.py install
    cd /var/lib/shaddock/ && ./set_ip.sh && cd -
    shaddock build all
    shaddock start all


Docker installation
~~~~~~~~~~~~~~~~~~~
https://docs.docker.com/installation/

Shaddock installation
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/epheo/shaddock
    sudo python setupy.py install


OpenStack template installation and configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reference template for an OpenStack platform:

.. code:: bash

    git clone https://github.com/epheo/shaddock-openstack /var/lib/shaddock/


The general architecture of the platform is defined in *infrastructure.yaml*
All the configurations (passwords, users, etc) are in *configuration.yaml*

.. code:: bash

	/var/lib/shaddock/etc/infrastructure.yaml
	/var/lib/shaddock/etc/configuration.yaml


This template contain the main modules of an OpenStack infrastructure. You
can/should edit it and add your Dockerfiles or images.

Structures example of *infratructure.yaml*:

.. code:: yaml

    - name: nova
      image: shaddock/nova
      priority: 40
      ports:
        - 8774
        - 8775
      volumes:
        - mount: /var/log/nova
          host_dir: /var/log/shaddock/nova
      privileged: True
      depends-on:
        - {name: seed, status: stopped}
        - {name: mysql, port: 3306}
        - {name: rabbitmq, port: 5672}
        - {name: keystone, port: 5000, get: '/v2.0'}
        - {name: keystone, port: 35357, get: '/v2.0'}


Launch a simple OpenStack platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build all the images and start the services

.. code:: bash

    shaddock build all
    shaddock start all


Usage
-----

The containers stored in this yaml file can be launched via the command line or
the interactive shell.


.. code:: bash

    Commands:
      build    [name] all    Build a new (or all the) container(s).
      create   [name]        Create a new container
      list                   Show a list of Containers and details.
      logs     [name]        Display logs of a container
      remove   [name] all    Remove a (or all the) container(s).
      restart  [name]        Restart a container
      show     [name]        Show details about a container
      start    [name]        Start new container
      stop     [name]        Stop container
      pull     [name]        Pull a Docker image


.. code:: bash

    usage: shaddock [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
                    [--docker-host DOCKER_HOST]     
                                        IP/hostname to the Docker server API.
                                        Default: 'unix://var/run/docker.sock'
                                        (Env: DOCKER_HOST)

                    [--docker-version DOCKER_VERSION]  
                                        Docker API version number
                                        Default: '1.12'
                                        (Env: DOCKER_VERSION)

                    [--template-dir TEMPLATE_DIR]    
                                        Template directory to use.
                                        Default: '/var/lib/shaddock'
                                        (Env: SHDK_TEMPLATE_DIR)

INFORMATIONS
------------

License
~~~~~~~
Shaddock is licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License. You may obtain a
copy of the License at http://www.apache.org/licenses/LICENSE-2.0

References
~~~~~~~~~~

Docker-py API Documentation: http://docker-py.readthedocs.org/

OpenStack Official Documentation: http://docs.openstack.org/
