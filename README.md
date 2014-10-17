OctOpenStack
============

OctOpenStack provides an OpenStack platform deployed in Docker containers and who provides and manages Docker containers as cloud instances.

USAGE
------
	chmod +x octopenstack.py
	sudo ./octopenstack.py

**build:**
> sudo ./octopenstack.py build

Build the differents Docker containers and configure them to provide the differents OpenStack services.
You can find a list of the differents containers and add new ones by editing services.yaml
All the configuration of your future OpenStack Docker platform is done in configuration.yaml

**run:**
> sudo ./octopenstack.py run

This command will create and run the architecture of your plateform and all the network configuration.
A frontal HAproxy manage all the API calls and can provides HighAvailabilty for them with an second node.

Hypervisors can be addeds and specified as in any other OpenStack plateform by the CLI, Python API or Horizon Dashboard

**init:**
> sudo ./octopenstack.py init

This fonction initialise all the Databases.

**stop:**
> sudo ./octopenstack.py stop

Stop the OpenStack services.

**start:**
> sudo ./octopenstack.py start

Start OpenStack services if the platform exist, (please prefer 'run' if he doesn't)
in

**rm:**
> sudo ./octopenstack.py rm
Remove the services


CONFIGURATION
-------------
Docker instances are builds by templateds dockerfiles
You will found the Services Dockerfiles templates in 'dockerfiles/' and their configurations in the services.yaml file.

	services.yaml

	configuration.yaml

All your configurations from 


REQUIEREMENTS
-------------
> - Python2.7
> - Docker

> - pip install docker-py
> - pip install PyYaml

> - MySql Connector http://dev.mysql.com/downloads/connector/c/
> - oursql (pip install oursql)


INFORMATION
-----------
OpenSTack services are deployed in CentOS7 environments.

> MVC architecture model.

Logs
""""
You can found the differents logs files in /var/log/octopenstack
	tail -f /var/log/octopenstack/*.log

Contributing
""""""""""""
I'm really interested by any advice, idea, help, or contribution.

License
"""""""
Not yet decided.

TODO:
-----
> - HiPache for the high availability
> - Open containers in Tmux windows
> - Add proxy node
> - Add os ctl node
> - Change SH scripts by OS Python API call
> - Modif Dockerfiles > git sources (python:2-onbuild) ?
> - Pull images option from my repo
> - Reduce the MySql footprint (run conf in a docker container?)
> - Replace conf by YAML
> - 
> - 
> - 

DONE:
> - Add stop and rm Options
> - Change Name
> - Re-Organise files
> - 
> - 
> - 
> - 
> - 
> - 
> - 
> - 
> - 
> - 
> - 