#!/bin/bash

sudo apt update
sudo apt install -y libatlas-base-dev python3-venv

python3 -m venv .venv
source .venv/bin/activate

pipenv install

echo "******************************************************************************"
echo "* Make sure to create a settings.py {use settings.py.template as a template} *"
echo "* To start use: ./run.sh                                                     *"
echo "******************************************************************************"
