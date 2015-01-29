FROM octopenstack/oos-base:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>
# http://docs.openstack.org/icehouse/install-guide/install/yum/content/install_dashboard.html

# Install Horizon

RUN yum -y install memcached python-memcached mod_wsgi openstack-dashboard


#Setup supervisord
ADD supervisord.conf /etc/supervisord.conf

VOLUME  ["/var/log/horizon"]


EXPOSE 80
EXPOSE 11211

CMD ["/usr/bin/supervisord", "-n"]
