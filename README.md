py-devstack
===========

OpenStack developpement environement deployed in Docker containers by Python APIs

#### In developpement, Non-functional

Dockerfiles to create images for core OpenStack services

For now, configuration sh scripts are based on github.com/Nirmata/openstack 

> **Requirements:**
> - Docker
> - Docker-py



Build container images
----------------------
> python py-devstack.py build


Create container images
-----------------------
> python py-devstack.py create


Run OpenStack Environment
-------------------------
> python py-devstack.py start


This script will start the containers (and inject all the necessary information?). It will also create default tenants & users as well as run some basic tests. To change passwords etc.

> **TODO:**
> - HiPache for the high availability
> - Open containers in Tmux windows
> - Add proxy node
> - Add os ctl node
> - Change SH scripts by OS Python API call
> - Modif Dockerfiles > git sources (python:2-onbuild) ?
> - Pull images option from my repo