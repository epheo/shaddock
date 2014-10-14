FROM ubuntu:14.04
MAINTAINER Thibaut Lapierre <root@epheo.eu>

# Repo and packages
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y upgrade


#Install Supervisor OpenSSH vim
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server supervisor vim python-pip mysql-client mysql-common python-mysqldb

# #Setup sshd
# RUN mkdir -p /var/run/sshd && echo 'root:root' |chpasswd
# RUN mkdir -p ~/.ssh/ 
# ADD authorized_keys ~/.ssh/authorized_keys
# EXPOSE 22

#Setup supervisord
RUN mkdir -p /var/log/supervisor
