FROM centos:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

# OpenStack Repo and packages
RUN yum -y update

RUN yum -y install mysql MySQL-python yum-plugin-priorities
RUN yum -y install http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-3.noarch.rpm
RUN yum -y install http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-2.noarch.rpm
RUN yum -y install openstack-utils openstack-selinux

#Setup supervisord
RUN yum -y install python-setuptools
RUN easy_install pip
RUN pip install supervisor

RUN mkdir -p /var/log/supervisor

RUN yum -y upgrade