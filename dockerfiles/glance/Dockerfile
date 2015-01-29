FROM octopenstack/oos-base:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>
# http://docs.openstack.org/icehouse/install-guide/install/yum/content/glance-install.html

# Install Glance
RUN yum -y install openstack-glance python-glanceclient

#Setup supervisord
ADD supervisord.conf /etc/supervisord.conf

VOLUME  ["/var/log/glance"]

EXPOSE 9292
CMD ["/usr/bin/supervisord", "-n"]
