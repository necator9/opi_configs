#!/bin/bash

PATH_TO_DIR=/root/opi_config

if [ $# -eq 0 ] ; then
	echo "Usage:"
	echo "First arg - hostname, in format <[my_custom_name]-[number in range 2-254]>"
	echo "Second arg - gateway status, bool value <true | false>"
	echo "Example ./configure.sh bbb-110 true"
	exit 1
fi

hostnamectl set-hostname --static $1
hostnamectl
echo Hostname has been updated

NAME=$1
number=${NAME#*-}

GATEWAY=$2

# Wlan parameters
W_IP=10.10.10.$number
A_IP=10.0.0.$number

# Update params.conf
sed -i "s/W_IP=.*/W_IP=$W_IP/" $PATH_TO_DIR/params.conf
sed -i "s/A_IP=.*/A_IP=$A_IP/" $PATH_TO_DIR/params.conf
sed -i "s/GATEWAY=.*/GATEWAY=$GATEWAY/" $PATH_TO_DIR/params.conf
echo params.conf has been updated

# Update n_ping_wd.sh
mask=10.10.10.
IP_POOL="($mask$((number+1)) $mask$((number-1)))"
sed -i "s/IP_POOL=.*/IP_POOL=$IP_POOL/" $PATH_TO_DIR/params.conf
