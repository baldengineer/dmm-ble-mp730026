#!/bin/bash

sudo apt update
sudo apt install -y libatlas-base-dev python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

echo "******************************************************************************"
echo "* Make sure to create a settings.py {use settings.py.template as a template} *"
echo "* To start use: source ./run.sh                                              *"
echo "******************************************************************************"
