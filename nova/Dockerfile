FROM pydevstack/osbase:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

#install nova
RUN apt-get update
RUN apt-get install -y --force-yes nova-api nova-cert nova-conductor nova-consoleauth nova-novncproxy nova-scheduler python-novaclient

#Setup supervisord
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

VOLUME  ["/var/log/nova"]

# Add scripts
ADD run.sh /run.sh
ADD create_db.sh /create_db.sh
RUN chmod 755 ./*.sh

CMD ["/run.sh"]
