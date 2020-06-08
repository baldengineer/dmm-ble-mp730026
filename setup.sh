#!/bin/bash

sudo apt-get update
sudo apt-get install -y npm python3-venv

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cd web
npm install

node_modules/.bin/browserify source.js -o dmm.js
