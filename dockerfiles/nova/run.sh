#!/bin/bash
echo "Setting up nova"

HOST_NAME=${HOST_NAME:-"localhost"}
HOST_IP=${HOST_IP:-"127.0.0.1"}
MYSQL_DB=${MYSQL_DB:-"localhost"}
RABBITMQ_HOST=${RABBITMQ_HOST:-"localhost"}
RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD:-"password"}
NOVA_DBPASS=${NOVA_DBPASS:-"password"}
NOVA_PASS=${NOVA_PASS:-"password"}
ADMIN_PASS=${ADMIN_PASS:-"password"}

service nova-api restart >/dev/null 2>&1
service nova-cert restart >/dev/null 2>&1
service nova-consoleauth restart >/dev/null 2>&1
service nova-scheduler restart >/dev/null 2>&1
service nova-conductor restart >/dev/null 2>&1
service nova-novncproxy restart >/dev/null 2>&1

echo "Removing nova DB..."
rm /var/lib/nova/nova.sqlite

echo "Updating conf file..."
echo "connection = mysql://nova:${NOVA_DBPASS}@${MYSQL_DB}/nova" >> /etc/nova/nova.conf
echo "rpc_backend = rabbit" >> /etc/nova/nova.conf
echo "rabbit_host = ${RABBITMQ_HOST}" >> /etc/nova/nova.conf
echo "rabbit_password = ${RABBITMQ_PASSWORD}" >> /etc/nova/nova.conf
echo "my_ip = ${HOST_IP}" >> /etc/nova/nova.conf
echo "vncserver_listen = ${HOST_IP}" >> /etc/nova/nova.conf
echo "vncserver_proxyclient_address  = ${HOST_IP}" >> /etc/nova/nova.conf
echo "auth_strategy = keystone" >> /etc/nova/nova.conf

echo "[keystone_authtoken]" >> /etc/nova/nova.conf
echo "auth_uri = http://${HOST_NAME}:5000/v2.0" >> /etc/nova/nova.conf
echo "auth_host = ${HOST_NAME}" >> /etc/nova/nova.conf
echo "auth_port = 35357" >> /etc/nova/nova.conf
echo "auth_protocol = http" >> /etc/nova/nova.conf
echo "admin_tenant_name = admin" >> /etc/nova/nova.conf
echo "admin_user = admin" >> /etc/nova/nova.conf
echo "admin_password = ${ADMIN_PASS}" >> /etc/nova/nova.conf

echo "auth_host = ${HOST_NAME}" >> /etc/nova/api-paste.ini
echo "auth_port = 35357" >> /etc/nova/api-paste.ini
echo "auth_protocol = http" >> /etc/nova/api-paste.ini
echo "auth_uri = http://${HOST_NAME}:5000/v2.0" >> /etc/nova/api-paste.ini
echo "admin_tenant_name = admin" >> /etc/nova/api-paste.ini
echo "admin_user = admin" >> /etc/nova/api-paste.ini
echo "admin_password = ${ADMIN_PASS}" >> /etc/nova/api-paste.ini



echo "Restarting nova..."
service nova-api restart >/dev/null 2>&1
service nova-cert restart >/dev/null 2>&1
service nova-consoleauth restart >/dev/null 2>&1
service nova-scheduler restart >/dev/null 2>&1
service nova-conductor restart >/dev/null 2>&1
service nova-novncproxy restart >/dev/null 2>&1

echo "Create database..."
./create_db.sh nova

echo "Create database tables"
su -s /bin/sh -c "nova-manage db sync" nova

#echo "Create nova user...""
#./create_user.sh nova

echo "Stopping nova..."
service nova-api stop >/dev/null 2>&1
service nova-cert stop >/dev/null 2>&1
service nova-consoleauth stop >/dev/null 2>&1
service nova-scheduler stop >/dev/null 2>&1
service nova-conductor stop >/dev/null 2>&1
service nova-novncproxy stop >/dev/null 2>&1

echo "Starting nova using supervisord..."
exec /usr/bin/supervisord -n
