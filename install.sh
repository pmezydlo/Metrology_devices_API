#!/bin/bash
apt-get install python3 python3-dev python3-pip
pip3 install -r requirements.txt
wget https://github.com/python-ivi/python-vxi11/archive/master.zip
unzip master.zip
cd python-vxi11-master/
python3 setup.py install
mkdir files
