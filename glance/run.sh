#!/bin/bash
echo "Setting up glance"

HOST_NAME=${HOST_NAME:-"localhost"}
MYSQL_DB=${MYSQL_DB:-"localhost"}
RABBITMQ_HOST=${RABBITMQ_HOST:-"localhost"}
RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD:-"password"}
GLANCE_DBPASS=${GLANCE_DBPASS:-"password"}

service glance-registry restart >/dev/null 2>&1
service glance-api restart >/dev/null 2>&1

echo "Removing glance DB..."
rm /var/lib/glance/glance.sqlite

echo "Updating conf file..."
sed -i -e "s/^sqlite_db*/#sqlite_db/g" /etc/glance/glance-registry.conf
sed -i -e "s/^backend*/#backend = sqlalchemy/g" /etc/glance/glance-registry.conf
sed -i -e "s/#connection.*/connection = mysql:\/\/glance:${GLANCE_DBPASS}@${MYSQL_DB}\/glance/g" /etc/glance/glance-registry.conf

sed -i -e "s/^sqlite_db*/#sqlite_db/g" /etc/glance/glance-api.conf
sed -i -e "s/^backend*/#backend = sqlalchemy/g" /etc/glance/glance-api.conf
sed -i -e "s/#connection.*/connection = mysql:\/\/glance:${GLANCE_DBPASS}@${MYSQL_DB}\/glance/g" /etc/glance/glance-api.conf
sed -i -e "s/rabbit_host.*/rabbit_host = ${RABBITMQ_HOST}/g" /etc/glance/glance-api.conf
sed -i -e "s/rabbit_password.*/rabbit_password = ${RABBITMQ_PASSWORD}/g" /etc/glance/glance-api.conf

echo "Restarting glance"
service glance-registry restart >/dev/null 2>&1
service glance-api restart >/dev/null 2>&1

echo "Create database..."
./create_db.sh glance

echo "Create database tables"
su -s /bin/sh -c "glance-manage db_sync" glance

#echo "Create glance user...""
#./create_user.sh glance

echo "Stopping glance"
service glance-registry stop >/dev/null 2>&1
service glance-api stop >/dev/null 2>&1

echo "Starting glance using supervisord..."
exec /usr/bin/supervisord -n
