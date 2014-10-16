#!/bin/bash
echo "**** Building base..."
cd base
sudo docker build -t epheo/openstack-base .
cd ..
echo "*** Building mysql.."
cd mysql
sudo docker build -t epheo/os-mysql .
cd ..
echo "*** Building rabbitmq.."
cd rabbitmq
sudo docker build -t epheo/os-rabbitmq .
cd ..
echo "*** Building keystone..."
cd keystone
sudo docker build -t epheo/os-keystone .
cd ..
echo "*** Building glance..."
cd glance
sudo docker build -t epheo/os-glance .
cd ..
echo "*** Building nova..."
cd nova
sudo docker build -t epheo/os-nova . 
cd ..
echo "*** Building horizon..."
cd horizon
sudo docker build -t epheo/os-horizon . 
cd ..
echo "*** Build complete ***"
#echo "**** Pushing images..."
#sudo docker push epheo/openstack-base
#sudo docker push epheo/os-mysql
#sudo docker push epheo/os-rabbitmq                     
#sudo docker push epheo/os-keystone
#sudo docker push epheo/os-glance
#sudo docker push epheo/os-nova
#sudo docker push epheo/os-horizon
#echo "**** Pushing images completed ***"
