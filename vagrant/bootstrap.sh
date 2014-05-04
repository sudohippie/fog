#!/usr/bin/env bash
check_status(){
	if [ $? -ne 0 ];
	then 
		echo "Error while $1. Aborting script." 1>&2
		exit 1
	fi
}

apt-get update
check_status "apt-get update"

apt-get install -y git
check_status "install git"

apt-get install -y python-setuptools
check_status "install python setup"

easy_install pip
check_status "install pip"

#USER_HOME=$(getent passwd vagrant | cut -d: -f6)
#FOG_HOME="$USER_HOME/fog"
USER_HOME="/home/vagrant"
FOG_HOME="/home/vagrant/fog"
REQ="/home/vagrant/fog/requirements.txt"
FOG="/usr/local/bin/fog"

if [ -d "$USER_HOME" ];
then
	if [ -d "$FOG_HOME" ];
	then
		rm -rf $FOG_HOME
	fi
	git clone https://github.com/sudohippie/fog $FOG_HOME
	check_status "cloning repo"
else
	echo "Home folder:$USER_HOME could not be found. Exiting"
	exit 1
fi

if [ -d "$FOG_HOME" ];
then
	pip install -r $REQ
	check_status "install project requirements"
else
	echo "Fog home could not be found. Exiting"
	exit 1
fi

#cd "$($FOG_HOME "$0")"
#nosetests
echo "python $HOME/fog/fog/fog.py $1 $2 $3 $4" > $FOG
chmod a+x $FOG
