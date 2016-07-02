#!/bin/bash

echo "Welcome to the Harp experiment installation process."
echo "Checking for administrator privileges"

if [[ $EUID -ne 0 ]]; then
   echo "Please run the script with administrator privileges (try sudo ./install.py)" 1>&2
   exit 1
fi
echo "Administrator privileges verified"

echo "We will install the following packages: mongodb-org, meteor, curl and git. We will move app specific files into a folder called 'harp'. Proceed? (y/n)"
read foldercreation
if (foldercreation != 'y'); then
	echo "Exiting script..."
	exit 1
fi

if [ ! -d "harp" ]; then
  mkdir harp
fi

cd harp

echo "Checking for Meteor"
if type meteor > /dev/null; then
    echo "Meteor found."
else
    if type curl > dev/null; then
      echo "Curl found"
    else
        sudo apt-get install curl
    fi
    curl https://install.meteor.com/ | sh    
fi

echo "Checking for git"
if type git > /dev/null; then
    echo "git found."
else
	sudo apt-get install -y git
fi

echo "Checking for mongodb-org-tools"
if type mongoexport > /dev/null; then
  echo "mongodb-org-tools found"
else
  sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
  echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
  sudo apt-get update
  sudo apt-get install -y mongodb-org

echo "Copying files"
git clone https://github.com/CdavM/harp/ .
echo "Installation done. Please run the command 'sudo meteor --settings settings.json run --port 80' to start"
echo "Would you like us to run the command for you? (y/n)"
read runcommand
if (runcommand == 'y'); then
	meteor --settings settings.json run
fi
