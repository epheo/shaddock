FROM centos:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

# OpenStack Repo and packages
RUN yum -y update

RUN yum -y install mysql MySQL-python yum-plugin-priorities initscripts openssh-server
RUN yum -y install http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-3.noarch.rpm
RUN yum -y install http://ftp.astral.ro/mirrors/fedora/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
RUN yum -y install openstack-utils openstack-selinux

#Setup supervisord
RUN yum -y install python-setuptools
RUN easy_install pip
RUN pip install supervisor
RUN mkdir -p /var/log/supervisor

#Setup sshd
RUN mkdir -p /var/run/sshd && echo 'root:root' |chpasswd
RUN mkdir -p /.ssh/
ADD authorized_keys /.ssh/authorized_keys
RUN chmod 600 /.ssh/authorized_keys
RUN ssh-keygen -t rsa1  -N "" -f /etc/ssh/ssh_host_rsa_key
RUN ssh-keygen -t dsa   -N "" -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -t ecdsa -N "" -f /etc/ssh/ssh_host_ecdsa_key
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config
RUN sed -i s/"GSSAPIAuthentication yes"/"GSSAPIAuthentication no"/g /etc/ssh/sshd_config
RUN echo "AuthorizedKeysFile /.ssh/authorized_keys" >> /etc/ssh/sshd_config
EXPOSE 22

RUN yum -y upgrade

