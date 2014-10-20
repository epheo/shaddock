![alt text](https://raw.githubusercontent.com/Epheo/py-devstack/CentOS/documentation/images/octopenstack.png "OctOpenStack" )

OctOpenStack provides an [OpenStack](http://openstack.org) platform deployed in [Docker](http://docker.io) containers and who provides and manages Docker containers as cloud instances.

-------------

OctOpenStack
============

* [USAGE](#usage)
  * [build](#build)
  * [run](#run)
  * [init](#init)
  * [stop](#stop)
  * [start](#start)
  * [rm](#rm)
  * [ip](#ip)
* [CONFIGURATION](#configuration)
* [REQUIEREMENTS](#requierements)
* [INFORMATION](#information)
  * [Logs](#logs)
  * [Contributing](#contributing)
  * [License](#license)
* [BackLog](#backlog)
  * [Todo](#todo)
  * [Done](#done)
* [References](#references)
* [UML Architecture Diagram](#uml-architecture-diagram)

> **Note:** This program is in devellopment! Services auto configuration is broken since migration to CentOS7, you can SSH into containers by specifying an rsa key in base dockerfile directory to configure them. I'm actually working on it on "autoconfig" branch.

USAGE
------
> sudo ./octopenstack.py command [container]
Use command only to interact with all services, you can also specify a container name.

### build
> sudo ./octopenstack.py build

Build the differents Docker containers and configure them to provide the differents OpenStack services.
You can find a list of the differents containers and add new ones by editing services.yaml
All the configuration of your OpenStack Docker platform is done in configuration.yaml

### run
> sudo ./octopenstack.py run

This command will create and run the architecture of your plateform and all the network configuration.
A frontal HAproxy manage all the API calls and can provides HighAvailabilty for them with an second node.

Hypervisors can be addeds and specified as in any other OpenStack plateform by the CLI, Python API or Horizon Dashboard

### init
> sudo ./octopenstack.py init

This fonction initialise all the Databases.

### {stop, start}
> sudo ./octopenstack.py stop

Stop the OpenStack services.

> sudo ./octopenstack.py start

Start OpenStack services if the platform exist, (please prefer 'run' if he doesn't)

### rm
> sudo ./octopenstack.py rm
Remove the services

### ip
> sudo ./octopenstack.py ip
Display services IP address 

CONFIGURATION
-------------

	- services.yaml
	- configuration.yaml

The general architecture of the platform is defined in `services.yaml` 
All the configurations (passwords, users, etc.) are in `configuration.yaml`

Both are in [YAML](http://www.yaml.org/)

Docker instances are builds by templateds dockerfiles
You will find the Services Dockerfiles templates in 'dockerfiles/'

REQUIEREMENTS
-------------
- [Docker](https://docs.docker.com/installation/archlinux/)
- Docker Python API: `pip install docker-py`
- PyYaml: `pip install PyYaml`


INFORMATION
-----------
- OpenSTack services are deployed in CentOS7 environments.
- MVC architecture model.

### Logs
You can found the differents logs files in /var/log/octopenstack
	tail -f /var/log/octopenstack/*.log

### Contributing
I'm really interested by any advice, idea, help, or contribution.

### License
OctOpenStack is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0


BackLog
-------
###Todo
- HiPache for the high availability
- Open containers in Tmux windows
- Add proxy node
- Add os ctl node
- Change SH scripts by OS Python API call
- Modif Dockerfiles > git sources (python:2-onbuild) ?
- Pull images option from my repo
- Reduce the MySql footprint (run conf in a docker container?)
- Replace conf by YAML

###Done
- Add stop and rm Options
- Change Name
- Re-Organise files


References
----------
- [OpenStack yum Install Guide](http://docs.openstack.org/icehouse/install-guide/install/yum/content/)
- [Docker-py API Docuementation](https://github.com/docker/docker-py/blob/master/README.md)

UML Architecture Diagram
------------------------
```sequence
Nova->MySql: :3306
Glance->MySql: :3306
Glance->RabbitMQ: :5672
Glance->Nova: :8774
Keystone->MySql: :3306
Keystone->Nova: :8774
```
> **Note:** Incomplete