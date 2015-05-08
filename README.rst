**Shaddock**
============
Shaddock provides a platform deployed in http://docker.com containers following
a predefined template (like an http://openstack.org infrastructure)

QuickStart
----------

.. code:: bash

    # Installation:
    git clone https://github.com/epheo/shaddock &&\
    sudo python setup.py install

    # Configuration
    cd /examples && ./set_ip.sh openstack.yml

    # Usage:
    shaddock -f examples/openstack.yml
    (shaddock) ps
    (shaddock) pull all
    (shaddock) start all

**Run the shaddock shell in a container:**

Without installation but require the docker API to listen on a tcp port.

.. code:: bash

    docker run --rm -i -v examples:/examples --env DOCKER_HOST="https://<docker_api>:2376" --env TEMPLATE_FILE=/examples/openstack.yml -t shaddock/shaddock



OpenStack template installation and configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reference template for an OpenStack platform:

.. code:: bash

    git clone https://github.com/epheo/shaddock-openstack /var/lib/shaddock/


The general architecture of the platform is defined in *infrastructure.yaml*

.. code:: bash

	/var/lib/shaddock/infrastructure.yaml
	/var/lib/shaddock/configuration.yaml


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

    shaddock pull all
    shaddock start all


Usage
-----

The containers stored in this yaml file can be launched via the command line or
the interactive shell.


.. code:: bash

    usage: shaddock [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
                    [--docker-host DOCKER_HOST] [--docker-version DOCKER_VERSION]
                    [-f TEMPLATE_FILE] [-d IMAGES_DIR]


.. code:: bash

    optional arguments:
      --version             Show program's version number and exit.
      -v, --verbose         Increase verbosity of output. Can be repeated.
      --log-file LOG_FILE   Specify a file to log output. Disabled by default.
      -q, --quiet           Suppress output except warnings and errors.
      -h, --help            Show this help message and exit.
      --debug               Show tracebacks on errors.
      --docker-host DOCKER_HOST
                            IP/hostname to the Docker API. (Env: DOCKER_HOST)
      --docker-version DOCKER_VERSION
                            Docker API version number (Env: DOCKER_VERSION)
      -f TEMPLATE_FILE, --template-file TEMPLATE_FILE
                            Template file to use. (Env: TEMPLATE_FILE)
      -d IMAGES_DIR, --images-dir IMAGES_DIR
                            Directory to build Docker images from.(Env:
                            IMAGES_DIR)


.. code:: bash

    Commands:
      build          Build a new container
      create         Create a new container
      help           print detailed help for another command
      info           Show details about a container
      list           Show a list of Containers.
      logs           Display the logs of a container
      ps             Show a list of Containers.
      pull           Pull a container from the Docker Repository
      remove         Remove a container
      restart        Restart a container
      show           Show details about a container
      start          Start a new container
      stop           Stop a container


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

Help
~~~~

**Set up the Docker remote API:**

refs: https://docs.docker.com/reference/api/docker_remote_api/


.. code:: bash

    cat /etc/default/docker.io
    DOCKER_OPTS="-H tcp://0.0.0.0:2376 -H unix:///var/run/docker.sock"


**Docker installation:**

refs: https://docs.docker.com/installation/
