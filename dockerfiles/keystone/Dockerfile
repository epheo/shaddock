FROM octopenstack/oos-base:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>
# http://docs.openstack.org/icehouse/install-guide/install/yum/content/keystone-install.html

# Install Keystone
RUN yum -y install openstack-keystone python-keystoneclient

ADD supervisord.conf /etc/supervisord.conf

VOLUME  ["/var/log/keystone"]

EXPOSE 35357
EXPOSE 5000

CMD ["/usr/bin/supervisord", "-n"]
