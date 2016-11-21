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
    shaddock -f openstack-deployer.yml
    (shaddock) ps
    (shaddock) build 
    (shaddock) start 


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
           - name: nova-builder
             image: shaddock/generic-pyvenv-builder:latest
             priority: 10
             volumes:
               - mount: /opt/openstack
                 host_dir: /opt/openstack
             env:
               GIT_URL: https://github.com/openstack/nova.git
               GIT_BRANCH: '{{ git_branch }}'
             command: builder.sh
   

Using the !include functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Shaddock allow you to split your definition model into multiple yaml files
using the !include notation.

This, conbined with the templating allow you to design very complex
architectures without repetitions or loosing in readabality of your model.


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
      command: "glance-api --log-file=/var/log/glance/glance-api.log"


How does the **scheduler** works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Shaddock scheduler will ensure that all the requirements you provide are 
matched before starting a new service.

You can check:
- A container status
- If a port is open (tcp or udp)
- The return code of a http GET

You can also specify the number of retry, the time to wait before 2 checks, and
if the check should use the system proxy vars or not.

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
The only prerequirements for a host to be part of a Shaddock cluster is toi
have the Docker API installed and listening on a port.
You can then configure your hosts in your cluster defintion.

.. code-block:: yaml

   hosts:
      - name: node001-socket
        url: unix://var/run/docker.sock
      
      - name: node002-tcp
        url: tcp://127.0.0.1:2376
        verion: 1.12

      - name: node003-tls
        url: tcp://127.0.0.1:2376
        tls: False
        cert_path: None
        key_path: None
        cacert_path: None
        tls_verify: False


Using the templating functionalities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The model definition variables {{ your_var }} are templated using Jinja2
before being interpreted by Shaddock.
You can define any variables value in the **vars:** section of a cluster
definiton.

refs: http://jinja.pocoo.org/


CLI usage:
----------

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


You can force a certain host API via the CLI or environment variables as well, 
both will take precedence over any host defintion from the model.


.. code:: raw

    usage: shaddock [--version] [-v] [--log-file LOG_FILE] [-q] [--debug]

                    [-f TEMPLATE_FILE] [-d IMAGES_DIR]

                    [-i --host] [--docker-version ]
                    [--tls ] [--tlscert ] [--tlskey ]
                    [--tlsverify ] [--tlscacert ]  


.. code:: bash

      export DOCKER_HOST='tcp://127.0.0.1:2376'
      export DOCKER_VERSION=1.12

      export DOCKER_TLS=True
      export DOCKER_CERT_PATH=/path/to
      export DOCKER_KEY_PATH=/path/to

      export DOCKER_TLS_VERIFY=True
      export DOCKER_CACERT_PATH=/path/to


Alternative configuration and other systems
-------------------------------------------

Docker Machine and OS X support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Please use `--boot2docker`

You may want to eval `$(sudo docker-machine env machine_name)"` first.


Run the shaddock shell from a container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: bash

    docker run --rm -i -v shaddock/tests/model/:/model \
        --env DOCKER_HOST="https://<your_host>:2376" \
        --env TEMPLATE_FILE=/model/service-tests.yml \
        -t shaddock/shaddock

Help
~~~~
**Set up the Docker API to listen on tcp:**
refs: https://docs.docker.com/reference/api/docker_remote_api/


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


