FROM epheo/openstack-base:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y qemu-kvm nova-compute-kvm
RUN dpkg-statoverride  --update --add root root 0644 /boot/vmlinuz-$(uname -r)

RUN mkdir -p /root/qemu
ADD kvm-mknod.sh /root/qemu/kvm-mknod.sh
ADD entrypoint.sh /root/qemu/entrypoint.sh
RUN chmod +x /root/qemu/*.sh

#Setup supervisord
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

VOLUME  ["/var/log/nova"]

# Add scripts
ADD run.sh /run.sh
ADD create_db.sh /create_db.sh
RUN chmod 755 ./*.sh

CMD ["/run.sh"]
