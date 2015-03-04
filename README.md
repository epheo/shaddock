Panama provides a platform deployed in [Docker](http://docker.io) containers following a predefined template (like a basic [OpenStack](http://openstack.org) infrastructure.)

-------------

Panama
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
* [INFORMATIONS](#informations)
  * [Contributing](#contributing)
  * [License](#license)
* [References](#references)

USAGE
-----
> ```usage: panama [-h] [-b [service_name]] [-c [service_name]] [-s [service_name]] [-k [service_name]] [-i [service_name]] [-n [service_name]]```

Panama need **sudo** rights.

A basic infrastructure template can be found in [Panama-template](https://github.com/Epheo/panama-template) repository.
This template deploy a basic OpenStack infrastructure. You can/should edit it in ```/var/lib/panama``` you'll find the differents OpenStack services with their Dockerfiles and ```etc``` directory.

## build
> ```--build [service_name]```

## create
> ```--create [service_name]```

## start
> ```--start [service_name]```

## stop
> ```--stop [service_name]```

## info
> ```--info [service_name]```

## remove
> ```--rm [service_name]```

CONFIGURATION
-------------
	- services.yaml
	- configuration.yaml

The general architecture of the platform is defined in `services.yaml` 
All the configurations (passwords, users, etc.) are in `configuration.yaml`

Both are in [YAML](http://www.yaml.org/)

In order to use Panama with a distant server or on **Mac OS** with boot2docker you can change the address in configuration.yaml

REQUIEREMENTS
-------------
- [Docker](https://docs.docker.com/installation/archlinux/)
- Docker Python API: `pip install docker-py`
- PyYaml: `pip install PyYaml`

INFORMATIONS
------------
## Contributing
I'm really interested in any advice, idea, help, or contribution.

## License
Panama is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

References
----------
- [OpenStack yum Install Guide](http://docs.openstack.org/icehouse/install-guide/install/yum/content/)
- [Docker-py API Documentation](https://github.com/docker/docker-py/blob/master/README.md)
