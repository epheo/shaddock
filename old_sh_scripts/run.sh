#!/bin/bash
echo "Stopping all containers..."
sudo docker stop  $(sudo docker ps | grep -v 'CONTAINER'  |gawk '{print $1}')


export HOST_NAME=$1
export HOST_IP=$2
export KEYSTONE_PASS="password"
export GLANCE_PASS="password"
export NOVA_PASS="password"
export ADMIN_TOKEN="password"
export ADMIN_PASSWORD=${ADMIN_TOKEN}
export KEYSTONE_HOST=${HOST_NAME}
export RABBITMQ_HOST=${HOST_NAME}
export RABBITMQ_PASSWORD="password"
export MYSQL_PASS="password"
export MYSQL_HOST=${HOST_NAME}
export MYSQL_USER="admin"

echo "Starting MYSQL DB..."
sudo docker run -d -p 3306:3306 -e MYSQL_PASS=${MYSQL_PASS} epheo/os-mysql
echo "Starting RabbitMQ..."
sudo docker run -d -p  5672:5672 -p 15672:15672 -e RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD} -v /var/log/openstack/rabbitmq:/var/log/supervisor epheo/os-rabbitmq
sleep 10
echo "Starting keystone..."
sudo docker run -d -p 35357:35357 -p 5000:5000 -h="keystone" -e HOST_NAME=${HOST_NAME} -e MYSQL_DB=${MYSQL_HOST} -e MYSQL_USER=${MYSQL_USER} -e MYSQL_PASSWORD=${MYSQL_PASS} \
    -e ADMIN_TOKEN=${ADMIN_TOKEN} -e KEYSTONE_DBPASS=${MYSQL_PASS} -v /var/log/openstack/keystone:/var/log/supervisor epheo/os-keystone 
sleep 5
echo "Starting glance"
sudo docker run -d -p 9292:9292 -h="glance" -e HOST_NAME=${HOST_NAME} -e MYSQL_DB=${MYSQL_HOST} -e MYSQL_USER=${MYSQL_USER} -e MYSQL_PASSWORD=${MYSQL_PASS} \
    -e RABBITMQ_HOST=${RABBITMQ_HOST} -e RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD} -e GLANCE_DBPASS=${MYSQL_PASS} -v /var/log/openstack/glance:/var/log/supervisor epheo/os-glance 
sleep 5
echo "Starting nova"
sudo docker run -d -p 8774:8774 -p 8775:8775 -h="nova" -e HOST_NAME=${HOST_NAME} -e HOST_IP=${HOST_IP} -e MYSQL_DB=${MYSQL_HOST} -e MYSQL_USER=${MYSQL_USER} -e MYSQL_PASSWORD=${MYSQL_PASS} \
    -e RABBITMQ_HOST=${RABBITMQ_HOST} -e RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD} -e NOVA_DBPASS=${MYSQL_PASS} -e ADMIN_PASS=${ADMIN_PASSWORD} --privileged -v /var/log/openstack/nova:/var/log/supervisor epheo/os-nova
sleep 5
echo "Starting horizon"
sudo docker run -d -p 80:80 -p 11211:11211 -h="horizon" -v /var/log/openstack/horizon:/var/log/supervisor -v /var/log/openstack/apache2:/var/log/apache2 -e HOST_NAME=${HOST_NAME} epheo/os-horizon

echo "** Setting up defaults..."
./create_default_user.sh
keystone/create_user.sh keystone ${HOST_NAME}
keystone/register_service.sh keystone ${HOST_NAME}
glance/create_user.sh glance ${HOST_NAME}
glance/register_service.sh glance ${HOST_NAME}
nova/create_user.sh nova ${HOST_NAME}
nova/register_service.sh nova ${HOST_NAME}

echo "** Testing..."
cd test
./keystone_test.sh ${HOST_NAME}
./glance_test.sh ${HOST_NAME}
cd ..
echo "** Testing completed"
