#!/bin/bash
echo "Setting up keystone..."

HOST_NAME=${HOST_NAME:-"localhost"}
MYSQL_DB=${MYSQL_DB:-"localhost"}
ADMIN_TOKEN=${ADMIN_TOKEN:-"password"}
KEYSTONE_DBPASS=${KEYSTONE_DBPASS:-"password"}

service keystone start >/dev/null 2>&1

echo "Removing keystone DB"
rm /var/lib/keystone/keystone.db

echo "Updating conf file..."
sed -i -e "s/#admin_token=ADMIN/admin_token = ${ADMIN_TOKEN}/g" /etc/keystone/keystone.conf 
sed -i -e "s/^connection.*/connection = mysql:\/\/keystone:${KEYSTONE_DBPASS}@${MYSQL_DB}\/keystone/g" /etc/keystone/keystone.conf
sed -i -e "s/#log_dir.*/log_dir = \/var\/log\/keystone/g" /etc/keystone/keystone.conf

echo "Restarting keystone"
service keystone restart >/dev/null 2>&1

echo "Create database..."
./create_db.sh keystone

echo "Create database tables"
su -s /bin/sh -c "keystone-manage db_sync" keystone

echo "Stopping keystone"
service keystone stop >/dev/null 2>&1

echo "Starting keystone using supervisord..."
exec /usr/bin/supervisord -n
