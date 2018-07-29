#!/bin/bash
apt-get install python3 python3-dev python3-pip
pip3 install -r requirements.txt
wget https://github.com/python-ivi/python-vxi11/archive/master.zip
unzip master.zip
python3 python-vxi11-master/setup.py install
mkdir files

crontab -l > cronscript
echo "@reboot sh $PWD/launcher.sh > $PWD/files/cronlog 2>&1" >> cronscript
crontab cronscript
rm cronscript


