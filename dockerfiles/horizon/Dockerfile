FROM octopenstack/osbase:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>
# http://docs.openstack.org/icehouse/install-guide/install/yum/content/install_dashboard.html

# Install Horizon

RUN yum -y install memcached python-memcached mod_wsgi openstack-dashboard


#Setup supervisord
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

VOLUME  ["/var/log/horizon"]

# Add scripts
ADD run.sh /run.sh
RUN chmod 755 ./*.sh

EXPOSE 80
EXPOSE 11211

CMD ["/run.sh"]
