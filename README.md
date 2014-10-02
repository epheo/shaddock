py-devstack
===========

Python Docker OpenStack Developpement Containers

> In Developpement non-functional

Dockerfiles to create images for core OpenStack services

For now, all the Dokerfiles based on github.com/Nirmata/openstack 

TODO:
- All services deployed from sources on a Python Docker base image
- Deployment of the services with Fabric and Docker Python API.
- SupervisorD ensure all the different process are running?
- HiPache for the high availability

To build container images:
$ fab localhost buil

To run openstack:
$ fab localhost run

This script will start the containers and inject all the necessary information. It will also create default tenants & users as well as run some basic tests. To change passwords etc, update the fabfile.py
