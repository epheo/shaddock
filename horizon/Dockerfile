FROM pydevstack/osbase:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

# http://docs.openstack.org/icehouse/install-guide/install/yum/content/install_dashboard.html

RUN yum -y install memcached python-memcached mod_wsgi openstack-dashboard
#sed -i -e "s/^OPENSTACK_HOST.*/OPENSTACK_HOST = \"${HOST_NAME}\"/g" /etc/openstack-dashboard/local_settings.py


#install horizon
#RUN apt-get update
RUN apt-get install -y --force-yes apache2 memcached libapache2-mod-wsgi openstack-dashboard
RUN apt-get remove -y --force-yes --purge openstack-dashboard-ubuntu-theme

#Setup supervisord
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

VOLUME  ["/var/log/horizon"]

# Add scripts
ADD run.sh /run.sh
RUN chmod 755 ./*.sh

EXPOSE 80
EXPOSE 11211

CMD ["/run.sh"]
