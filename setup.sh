#!/bin/bash

#mongodb
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list
sudo apt-get update
sudo apt-get install mongodb-10gen

#rethinkdb
sudo add-apt-repository ppa:rethinkdb/ppa
sudo apt-get update
sudo apt-get install rethinkdb

sudo pip install pymongo
sudo pip install rethinkdb
