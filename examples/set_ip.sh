#!/bin/bash

IP=`ip route get 8.8.8.8 | awk 'NR==1 {print $NF}'`
sed -i s/\<host\>/$IP/g $1

