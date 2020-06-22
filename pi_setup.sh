#!/bin/bash

sudo apt update
sudo apt install -y npm libatlas-base-dev python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cd web
# Build dmm.js
# npm install
# node_modules/.bin/browserify source.js -o dmm.js

# Grab from Geekboy's server instead of building
wget http://dmm.keepdream.in/dmm.js

echo "******************************************************************************"
echo "* Make sure to create a settings.py {use settings.py.template as a template} *"
echo "* To start use: source ./run.sh                                              *"
echo "******************************************************************************"
