FROM py-devstack/osbase:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

# Keystone packages
RUN apt-get update
RUN apt-get install -y --force-yes keystone python-keystone
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

VOLUME  ["/var/log/keystone"]

# Add scripts
ADD run.sh /run.sh
ADD create_db.sh /create_db.sh
RUN chmod 755 ./*.sh

CMD ["/run.sh"]

