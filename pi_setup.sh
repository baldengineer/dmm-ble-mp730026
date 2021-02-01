#!/bin/bash

sudo apt update
sudo apt install -y libatlas-base-dev python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

echo "******************************************************************************"
echo "* Make sure to create a settings.py {use settings.py.template as a template} *"
echo "******************************************************************************"
read -p "Do You want to install this as a system service? (y/n)" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo cp dmm-ble-mp730026.service /etc/systemd/system/dmm-ble-mp730026.service
	sudo sed  "s|WorkingDirectory.*|WorkingDirectory=$PWD|" -i /etc/systemd/system/dmm-ble-mp730026.service
	sudo sed  "s|ExecStart.*|ExecStart=$PWD/.venv/bin/python3 main.py|" -i /etc/systemd/system/dmm-ble-mp730026.service
	sudo systemctl enable dmm-ble-mp730026.service
	sudo systemctl start dmm-ble-mp730026
	echo "******************************************************************************"
	echo "* Service installed and started                                              *"
	echo "* Check sudo journalctl -u dmm-ble-mp730026.service for errors               *"
	echo "******************************************************************************"
else
	echo "******************************************************************************"
	echo "* To start use: source ./run.sh                                              *"
	echo "******************************************************************************"
fi


