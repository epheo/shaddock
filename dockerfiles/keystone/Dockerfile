FROM octopenstack/oos-base:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>
# http://docs.openstack.org/icehouse/install-guide/install/yum/content/keystone-install.html

# Install Keystone
RUN yum -y install openstack-keystone python-keystoneclient

ADD supervisord.conf /etc/supervisord.conf

VOLUME  ["/var/log/keystone"]

# Add scripts
ADD run.sh /run.sh
ADD create_db.sh /create_db.sh
RUN chmod 755 ./*.sh

EXPOSE 35357
EXPOSE 5000

CMD ["/run.sh"]

