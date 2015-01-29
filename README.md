![alt text](https://raw.githubusercontent.com/Epheo/octopenstack/master/documentation/images/octopenstack.png "OctOpenStack" )

OctOpenStack provides an [OpenStack](http://openstack.org) platform deployed in [Docker](http://docker.io) containers and witch provides and manages Docker containers as cloud instances.

-------------

OctOpenStack
============

* [USAGE](#usage)
  * [Build](#build)
  * [Create](#create)
  * [Start](#start)
  * [Stop](#stop)
  * [Info](#info)
  * [Remove](#rm)
* [CONFIGURATION](#configuration)
* [REQUIEREMENTS](#requierements)
* [INFORMATION](#information)
  * [Logs](#logs)
  * [Contributing](#contributing)
  * [License](#license)
* [References](#references)

> **Note:** This program is in development! Services auto configuration is broken since migration to CentOS7.


```sudo python setup.py install``` ou ```sudo pip install octopenstack```

USAGE
------
> ```usage: octopenstack [-h] [-b [service_name]] [-c [service_name]] [-s [service_name]] [-k [service_name]] [-i [service_name]] [-n [service_name]]```

Run without [service_name] for all services:
> ```octopenstack -b```

Octopenstack need **sudo** rights.

Use command only to interact with all services, you can also specify a container name.

### build
> ```-b [service_name], ```  
> ```--build [service_name]```

Build the different Docker containers and configure them to provide the different OpenStack services.
You can find a list of the different containers and add new ones by editing services.yaml
All the configuration of your OpenStack Docker platform is done in configuration.yaml

### create
> ```-c [service_name], ```  
> ```--create [service_name]```

This command will the architecture of your platform and all the network configuration.
A frontal HAproxy manage all the API calls and can provides HighAvailability for them with an second node.

Hypervisors can be added and specified as in any other OpenStack platform by the CLI, Python API or Horizon Dashboard


### start
> ```-s [service_name], ```  
> ```--start [service_name]```

Start OpenStack services if the platform exist, (if not, run 'create')


## stop
> ```-k [service_name], ```  
> ```--stop [service_name]```

Stop the OpenStack services.


## info
> ```-i [service_name], ```  
> ```--info [service_name]```

Get containers information

## remove
> ```-r [service_name], ```  
> ```--rm [service_name]```

Remove containers

CONFIGURATION
-------------
	- services.yaml
	- configuration.yaml

The general architecture of the platform is defined in `services.yaml` 
All the configurations (passwords, users, etc.) are in `configuration.yaml`

Both are in [YAML](http://www.yaml.org/)

Docker instances are (will be :) ) builds by templated dockerfiles
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
You can found the different logs files in /var/log/octopenstack
	> tail -f /var/log/octopenstack/*.log

### Contributing
I'm really interested in any advice, idea, help, or contribution.

### License
OctOpenStack is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0


References
----------
- [OpenStack yum Install Guide](http://docs.openstack.org/icehouse/install-guide/install/yum/content/)
- [Docker-py API Documentation](https://github.com/docker/docker-py/blob/master/README.md)
