**Shaddock**
============
Shaddock provides a platform deployed in http://docker.com containers following a predefined template (like a basic http://openstack.org infrastructure.)


Usage
-----
A basic infrastructure template can be found in the Shaddock OpenStack template repository: https://github.com/epheo/shaddock-openstack
This template deploy a basic OpenStack infrastructure. You can/should edit it in **/var/lib/shaddock**

Common commands are:
    - build [service_name]
    - create [service_name]
    - start [service_name]
    - stop [service_name]
    - list
    - show [service_name]
    - remove [service_name]

QuickStart
----------

Docker installation
~~~~~~~~~~~~~~~~~~~
https://docs.docker.com/installation/


Shaddock installation
~~~~~~~~~~~~~~~~~~~~~

    sudo pip install shaddock

or

    sudo python setupy.py install


OpenStack template installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reference template for an OpenStack platform

    git clone https://github.com/epheo/shaddock-openstack /var/lib/shaddock/


Configuration
~~~~~~~~~~~~~

	- /var/lib/shaddock/services.yaml
	- /var/lib/shaddock/configuration.yaml

The general architecture of the platform is defined in *services.yaml*
All the configurations (passwords, users, etc.) are in *configuration.yaml*

Note: Both are in YAML: http://www.yaml.org/

In order to use Shaddock with a distant server or on Mac OS with boot2docker you can change the address in configuration.yaml

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


INFORMATIONS
------------

License
~~~~~~~
Shaddock is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

References
~~~~~~~~~~

    Docker-py API Documentation: http://docker-py.readthedocs.org/

    OpenStack Official Documentation: http://docs.openstack.org/