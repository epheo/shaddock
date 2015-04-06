**Shaddock**
============
Shaddock provides a platform deployed in http://docker.com containers following a predefined template (like a basic http://openstack.org infrastructure)

QuickStart
----------

Docker installation
~~~~~~~~~~~~~~~~~~~
https://docs.docker.com/installation/

Shaddock installation
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    sudo python setupy.py install

or

.. code:: bash

    sudo pip install shaddock

OpenStack template installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reference template for an OpenStack platform

.. code:: bash

    git clone https://github.com/epheo/shaddock-openstack /var/lib/shaddock/


Configuration
~~~~~~~~~~~~~
The general architecture of the platform is defined in *services.yaml*
All the configurations (passwords, users, etc.) are in *configuration.yaml*

.. code:: bash

	/var/lib/shaddock/etc/services.yaml
	/var/lib/shaddock/etc/configuration.yaml

Note: Both are in YAML http://www.yaml.org/

General shaddock configuration is in:

.. code:: bash

        /etc/shaddock/shaddock.conf


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
A basic infrastructure template can be found in the Shaddock OpenStack template repository: https://github.com/epheo/shaddock-openstack
This template deploy a basic OpenStack infrastructure. You can/should edit it in **/var/lib/shaddock**

Common commands are:

.. code:: bash

    (shaddock) build [service_name] [all]
    (shaddock) create [service_name]
    (shaddock) start [service_name]
    (shaddock) stop [service_name]
    (shaddock) list
    (shaddock) show [service_name]
    (shaddock) remove [service_name]
    (shaddock) logs [service_name]


INFORMATIONS
------------

License
~~~~~~~
Shaddock is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

References
~~~~~~~~~~

Docker-py API Documentation: http://docker-py.readthedocs.org/

OpenStack Official Documentation: http://docs.openstack.org/