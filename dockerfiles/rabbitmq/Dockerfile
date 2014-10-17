FROM ubuntu:14.04
MAINTAINER Thibaut Lapierre <root@epheo.eu>

# Install rabbitmq
RUN apt-get install -y --force-yes rabbitmq-server
RUN rabbitmq-plugins enable rabbitmq_management

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Add scripts
ADD run.sh /run.sh
RUN chmod 755 ./*.sh

EXPOSE 5672
EXPOSE 15672

CMD ["/run.sh"]
