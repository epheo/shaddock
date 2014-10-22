FROM octopenstack/oos-base:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

# Install rabbitmq
RUN yum install -y rabbitmq-server
#RUN rabbitmq-plugins enable rabbitmq_management

ADD supervisord.conf /etc/supervisord.conf

# Add scripts
ADD run.sh /run.sh
RUN chmod 755 ./*.sh

EXPOSE 5672
EXPOSE 15672

CMD ["/run.sh"]
