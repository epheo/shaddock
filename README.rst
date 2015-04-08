**Shaddock**
============
Shaddock provides a platform deployed in http://docker.com containers following
a predefined template (like an http://openstack.org infrastructure)

QuickStart
----------

Docker installation
~~~~~~~~~~~~~~~~~~~
https://docs.docker.com/installation/

Shaddock installation
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    sudo python setupy.py install


OpenStack template installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reference template for an OpenStack platform

.. code:: bash

    git clone https://github.com/epheo/shaddock-openstack /var/lib/shaddock/


Configuration
~~~~~~~~~~~~~
The general architecture of the platform is defined in *infrastructure.yaml*
All the configurations (passwords, users, etc) are in *configuration.yaml*

.. code:: bash

	/var/lib/shaddock/etc/infrastructure.yaml
	/var/lib/shaddock/etc/configuration.yaml

Note: Both are in YAML http://www.yaml.org/

General shaddock options are:

.. code:: bash

    --docker-host DOCKER_HOST
                        IP/hostname to the Docker server API. 
                        (Env: DOCKER_HOST)
                        Here: 'unix://var/run/docker.sock' by default.

    --docker-version DOCKER_VERSION
                        Docker API version number (Env: DOCKER_VERSION)
                        Here: '1.12' by default.

    --template-dir TEMPLATE_DIR
                        Template directory to use. (Env: SHDK_TEMPLATE_DIR)
                        Here: '/var/lib/shaddock' by default.


Launch a simple OpenStack platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build all the images and start the services

.. code:: bash

    shaddock
    (shaddock) build all
    (shaddock) start rabbitmq
    (shaddock) start mysql
    (shaddock) start keystone
    (shaddock) start seed
    (shaddock) start nova
    (shaddock) start glance
    (shaddock) start horizon


Usage
-----
A basic infrastructure template can be found in the Shaddock OpenStack template
repository: https://github.com/epheo/shaddock-openstack
This template deploy a basic OpenStack infrastructure. You can/should edit it 
in **/var/lib/shaddock**

Common commands are:

.. code:: bash

    usage: shaddock [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
                [--docker-host DOCKER_HOST] [--docker-version DOCKER_VERSION]
                [--template-dir TEMPLATE_DIR]


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
