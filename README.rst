**Shaddock**
============
Shaddock is a container based orchestration and deployment tool that rely on
a yaml definition model to describe and manage a distributed multi-service
infrastructure.

http://github.com/epheo/shaddock-openstack is a yml definition model exemple you
can use with Shaddock to build, deploy and manage the lifecycle of an OpenStack
platform from the upstream git sources.


QuickStart
----------

.. code:: bash

    # Shaddock installation:
    git clone https://github.com/epheo/shaddock
    cd shaddock && sudo pip install .

    # Using an existing yaml definition model:
    git clone https://github.com/epheo/shaddock-openstack

    # Play with it! :
    shaddock -f openstack-legacy.yml
    (shaddock) ps
    (shaddock) build all
    (shaddock) start all


The Shaddock YAML definiton model
---------------------------------

.. code-block:: yaml

   clusters: 
   
     - name: venv-builder
       hosts: !include hosts/all.yml
       vars:
         git_branch: 'stable/newton'
       images: images/venv-builder/
   
       services:       
           - name: nova
             image: shaddock/generic-pyvenv-builder:latest
             priority: 10
             volumes:
               - mount: /opt/openstack
                 host_dir: /opt/openstack
             env:
               GIT_URL: https://github.com/openstack/nova.git
               GIT_BRANCH: '{{ git_branch }}'
   

Using the jinja2 templating functionalities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The entire model is parsed using jinja2 before being interpreted by Shaddock,
You can define any variables in the ***vars:*** section of a cluster definiton.

refs: http://jinja.pocoo.org/


Using the !include functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Shaddock allow you to split your definition model into multiple yaml files using the !include fonction.

This, conbined with the Jinja2 templating allow you to design very complex architectures without repetitions or loosing in readabality of your model.


.. code-block:: yaml

   vars:
     git_branch: 'stable/newton'


.. code-block:: yaml

   vars: !include myfolder/vars_supertype.yml 

.. code-block:: bash

   $cat ./myfoler/vars_supertype.yml

   git_branch: 'stable/newton'


How to define a **service**
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: yaml

    - name: glance
      image: shaddock/glance:latest
      host: node0001
      priority: 50
      ports:
        - 9292
        - 4324
      volumes:
        - mount: /var/log/glance
          host_dir: /var/log/shaddock/glance
      depends-on:
        - {name: mysql, port: 3306}
        - {name: keystone, port: 5000, get: '/v2.0'}
        - {name: keystone, port: 35357, get: '/v2.0'}
      env:
        MYSQL_HOST_IP: '{{ your_ip }}'
        KEYSTONE_HOST_IP: '{{ your_ip }}'
        GLANCE_DBPASS: '{{ your_ip }}'
        GLANCE_PASS: '{{ your_ip }}'

How does the **scheduler** works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Shaddock scheduler will ensure that all the requirements you provide are matched before starting a new service.

You can check:
- A container status
- If a container listen or don't listen on a port (tcp or udp)
- The value returned by a http get

You can also specify the number of retry and the time to wait before 2 checks.


.. code:: yaml

     - {name: nova, status: stopped}
     - {name: nova, port: 8774, type: tcp}
     - {name: nova, port: 8774, state: down, type: tcp}
     - {host: google.com, port: 8774, state: down, type: tcp}
     - {name: nova, type: http, get: '/v2.0', port: 5000, code: 200}
     - {host: google.com, type: http, get: '/v2.0', port: 5000, code: 200}
     - {host: 127.0.0.1, type: http, get: '/', code: 200, useproxy: False }
     - {name: nova, sleep: 20} # defaults to 10
     - {name: nova, retry: 10} # defaults to 5


Multi-host capability
~~~~~~~~~~~~~~~~~~~~~
Shaddock is able to schedule your services on different hosts accros your 
datacenter.
The only prerequirements for a host to be part of a Shaddock cluster is to have
the Docker API installed and listening on a port.
You can then configure your hosts in your cluster defintion.

.. code-block:: yaml

   hosts:
     - name: localhost
       url: unix://var/run/docker.sock
     
     - name: node001
       url: tcp://10.0.42.1:4243

     - name: node002
       url: tcp://10.0.42.2:4243

The TLS options are currently only available via the CLI or the environment 
variables but will be added to the model in the next milestone.


CLI usage:
----------

.. code:: bash

    shaddock --help


.. code:: raw

    usage: shaddock [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
                    [-H DOCKER_HOST] [--tlscert DOCKER_CERT_PATH]
                    [--tlskey DOCKER_KEY_PATH] [--tlscacert DOCKER_CACERT_PATH]
                    [--tlsverify DOCKER_TLS_VERIFY] [--tls DOCKER_TLS]
                    [--docker-version DOCKER_VERSION] [-f TEMPLATE_FILE]
                    [-d IMAGES_DIR]


.. code:: raw

    optional arguments:
      --version             Show program's version number and exit.
      -v, --verbose         Increase verbosity of output. Can be repeated.
      --log-file LOG_FILE   Specify a file to log output. Disabled by default.
      -q, --quiet           Suppress output except warnings and errors.
      -h, --help            Show this help message and exit.
      --debug               Show tracebacks on errors.
      -H DOCKER_HOST, --host DOCKER_HOST
                            IP/hostname to the Docker API. (Env: DOCKER_HOST)
      --tlscert DOCKER_CERT_PATH
                            Path to TLS certificate file. (Env: DOCKER_CERT_PATH)
      --tlskey DOCKER_KEY_PATH
                            Path to TLS key file. (Env: DOCKER_KEY_PATH)
      --tlscacert DOCKER_CACERT_PATH
                            Trust only remotes providing a certificate signed by
                            theCA given here. (Env: DOCKER_CACERT_PATH)
      --tlsverify DOCKER_TLS_VERIFY
                            Use TLS and verify the remote. (Env:
                            DOCKER_TLS_VERIFY)
      --tls                 Use TLS; implied by tls-verify flags. (Env:
                            DOCKER_TLS)
      --boot2docker         Use Boot2Docker TLS conf. (Env: DOCKER_BOOT2DOCKER)
                            You should first: "eval $(sudo docker-machine env
                            machine_name)"
      --docker-version DOCKER_VERSION
                            Docker API version number (Env: DOCKER_VERSION)
      -f TEMPLATE_FILE, --template-file TEMPLATE_FILE
                            Template file to use. (Env: TEMPLATE_FILE)
      -d IMAGES_DIR, --images-dir IMAGES_DIR
                            Directory to build Docker images from.(Env:
                            IMAGES_DIR)


.. code:: raw

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


Alternative configuration and other systems
-------------------------------------------

Docker Machine and Mac OS X support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Please use `--boot2docker`

You may want to eval `$(sudo docker-machine env machine_name)"` first.


Run the shaddock shell from a container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Without installation but require the docker API to listen on a tcp port.

.. code:: bash

    docker run --rm -i -v examples:/examples --env DOCKER_HOST="https://<docker_api>:2376" --env TEMPLATE_FILE=/examples/openstack.yml -t shaddock/shaddock



Informations
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
