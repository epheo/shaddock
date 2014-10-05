py-devstack
===========

Py-Devstack provides OpenStack developpement environement deployed in Docker containers by Python APIs

You can use the provideds Dockerfiles to create images for core OpenStack services or use py-devstack to deploy the environement.

For now, configuration sh scripts are based on github.com/Nirmata/openstack and will be replaced by directs API calls


> **Requirements:**
> - Python2.7
> - Docker
> - Docker-py

Build contain er images
----------------------
> sudo python py-devstack.py build
 
Create container images
-----------------------
> sudo python py-devstack.py create


Run OpenStack Environment
-------------------------
> python py-devstack.py start

Configure Environments
----------------------

	./create_default_user.sh
	keystone/create_user.sh keystone ${HOST_NAME}
	keystone/register_service.sh keystone ${HOST_NAME}
	glance/create_user.sh glance ${HOST_NAME}
	glance/register_service.sh glance ${HOST_NAME}
	nova/create_user.sh nova ${HOST_NAME}
	nova/register_service.sh nova ${HOST_NAME}
	./keystone_test.sh ${HOST_NAME}
	./glance_test.sh ${HOST_NAME}



TODO:
-----
> - HiPache for the high availability
> - Open containers in Tmux windows
> - Add proxy node
> - Add os ctl node
> - Change SH scripts by OS Python API call
> - Modif Dockerfiles > git sources (python:2-onbuild) ?
> - Pull images option from my repo
