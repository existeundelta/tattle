#!/bin/bash
# spin up lemonade stand
# apt-get -y update && apt-get -y upgrade
apt-get -y install git python-pip unzip
git clone https://github.com/hollerith/tattle.git
cd tattle
pip install -r requirements.txt
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
python app.py &
./ngrok http -bind-tls=true 80

