#!/bin/bash

sudo apt update
sudo apt install -y libatlas-base-dev python3-venv
sudo apt install -y npm

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cd web
# Build dmm.js
npm install
node_modules/.bin/browserify source.js -o dmm.js

# Grab from webserver
# wget http://dmm.keepdream.in/dmm.js

echo "******************************************************************************"
echo "* Make sure to create a settings.py {use settings.py.template as a template} *"
echo "* To start use: source ./run.sh                                              *"
echo "******************************************************************************"
