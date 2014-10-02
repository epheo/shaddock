py-devstack
===========

Python Docker OpenStack Developpement Containers

#### In developpement, Non-functional

Dockerfiles to create images for core OpenStack services

For now, all the Dokerfiles and scripts are based on github.com/Nirmata/openstack 

> **TODO:**
> - All services deployed from sources on a Python Docker base image (python:2-onbuild)
> - Deployment of the services with Fabric and Docker Python API.
> - HiPache for the high availability


Requirements
------------
Python-fabric: https://github.com/fabric/fabric
Open-ssh: http://openssh.com/
Docker Python API: https://github.com/docker/docker-py


Build container images
----------------------
$ fab localhost buil


Run OpenStack
-------------
$ fab localhost run

SupervisorD ensure all the different process are running?
This script will start the containers and inject all the necessary information. It will also create default tenants & users as well as run some basic tests. To change passwords etc, update the fabfile.py

