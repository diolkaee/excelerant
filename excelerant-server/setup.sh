#!bin/bash

sudo pip3 install pyserial
mkdir pplv2
wget https://www.pixtend.de/files/downloads/pplv2_v0.1.x.zip
unzip pplv2_v0.1.x.zip -d ./pplv2/
cd pplv2
sudo python3 setup.py install
sudo python3 -m pip install -r requirements.txt