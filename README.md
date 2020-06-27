# dmm-ble-mp730026

[TOC]

 # About

Python code to access the a Multicomp Pro MP730026 DMM over BLE

This multimeter supports communication over Bluetooth, however, the official software is not very good. It only works with a specific dongle.

Using [the bleak python module](https://github.com/hbldh/bleak), virtually any operation system and Bluetooth controller works. So far I have successfully used this code with:

* **Linux: Raspberry Pi 3B, Raspberry Pi 4, Raspberry Pi0W**  *Recommended

* macOS: Macbook Pro and MacPro (Trashcan)

* Windows 10: Microsoft Surface Book Pro 2

  

The intent for the code is to provide an object representing the DMM.

bleak_scan.py can be used to find the MAC address of your meter.

## Installation

The recommended method for installing is to use git on a Raspberry Pi

```bash
git clone https://github.com/baldengineer/dmm-ble-mp730026.git
```

setup on Raspberry Pi:

```bash
cd ~/dmm-ble-mp730026
./pi_setup.sh
```

This will install the appropriate programs needed and create a python virtual environment 

**Note about `dmm.js`**

Building `dmm.js` requires installing node and some node modules to build it from source. The installation script pulls a current version from a hosted server.
If you would like to build `dmm.js` instead of downloading it, uncomment the *Build dmm.js* section and comment the *Grab from webserver* section in `pi_setup.sh` before running it.

## Before first run

Copy the `settings.py.template` to `settings.py` This file will not be over-written on updates.

The `multi_meters` is a comma separated list for each meter you wish to connect to. The template currently has *MP730026* as meter 0, and Demo as meter 1. 

See [Supported Meters](#supported-meters) for specific configurations to pass.

## Running

On Raspberry Pi, use:

```bash
cd ~/dmm-ble-mp730026
./run.sh
```

Will start up the websocket and Bluetooth services for getting data from the meter.

If you get a permissions error on Raspberry Pi see [Raspberry Pi Permissions](#raspberry-pi-permissions)

##  Advanced Usage

This library exposes a DMM object that exposes all the data for a mp730026 multimeter


```python
  self.address = address # Devices MAC address
  self.mode = False      # Current measurement Mode. EG AC voltage
  self.hold = False      # hold Flag
  self.rel = False       # rel Flag
  self.value = False     # String containing 4 digit and one decimal Value
  self.suffix = False    # String of data suffix. EG mV KΩ
  self.decimal = False   # Decimal Position
  self.negative = False  # If the number is a negative value
  self.autorange = False # Auto-range flag
  self.connected = False # Returns the status of the meter
  self.digits = 4        # The number of digits the meter can display
```



These values are updated by calling parse() with a raw byte array of the data from the DMM.

```python
DMM.parse([0x23, 0xF0, 0x04, 0x00, 0xDE, 0x85])

# this fills the object variables as such
mode = "DC volts"
hold = False
rel = False
value = -1.502
suffix = "V"
decimal = 1
negative = False
autorange = False
```



## Example URLs

Included is an example for connecting a meter to a web-socket for sending the data across the internet, In this case to a web page to show off the multimeter reading in real time.

### Accessing Live Data

Opening index.html either locally or hosted with the following flags

**websocketserver *required**

IP Address or Host name of server, eg 127.0.0.1, 192,168.1.100, raspberrypi

**websocketport**

Web socket port, defaults to 18881

**meter**

Give an integer value that matches the index in your settings.py. For the first meter use 0, second, 1, etc...

Defaults to meter 0 if no value is passed, or is an invalid value.

#### **background**

RGB syntax or [HTML color names](https://htmlcolorcodes.com/color-names/),

```html
rgb(250,128,114)
salmon
```

**oncolor**

Color of the darker background elements of the display

**offcolor**

Color of the brighter foreground elements



#### Examples

- http://127.0.0.1/index.html?websocketserver=127.0.0.1&websocketport=18881&background=grey&onColor=black&offColor=dimgrey
- http://localhost/?websocketserver=127.0.0.1&websocketport=18881&background=black&onColor=Lime&offColor=DarkGreen
- http://localhost/?websocketserver=127.0.0.1
- http://192.168.1.71/?websocketserver=192.168.1.71&websocketport=18881&meter=0



### Accessing Saved Data

Open saved.html either locally or hosted with the same flags as Accessing Live Data.

#### Examples

- http://127.0.0.1/saved.html?websocketserver=127.0.0.1
- http://192.168.1.71/saved.html?websocketserver=192.168.1.71&websocketport=18881&meter=0
- http://localhost/saved.html?websocketserver=127.0.0.1&websocketport=18881&background=black&onColor=Lime&offColor=DarkGreen

### OBS Browser Source

This was actually designed to be used with OBS as a browser source. The URL you generated above goes in URL height and width are as follows

```
width = 250
height = 85
```

All other defaults are fine.


### Raspberry Pi Permissions

Permissions for the Pi user to access Bluetooth are needed

```bash
sudo adduser pi bluetooth
```

Also you will need to modify a file according to [this post](https://www.raspberrypi.org/forums/viewtopic.php?p=746917&sid=d3eb670e77ee7fb900499168b1bc83d7#p746917)

### Hosting

The html interface can be locally provided to a web browser or OBS source. However if one desires to host it remotely a nginx file has been provided.

Install Nginx and link file

```bash
sudo apt-get install nginx
sudo rm /etc/nginx/sites-available/default # Warning: This will remove the default nginx page
ln ~/dmm-ble-mp730026/nginx-site /etc/nginx/sites-available/default
```

## Supported Meters

| Model    | Required Parameters | Optional Parameters | Settings.py Example           |
| -------- | ------------------- | ------------------- | ----------------------------- |
| MP730026 | MAC_Address         |                     | MP730026("AA:AA:AA:AA:AA:AA") |
| Demo     |                     | Name                | Demo(), Demo("My Demo")       |

Support for more meters is in progress. If you have a meter you would like to be supported, please check the [Issues](https://github.com/baldengineer/dmm-ble-mp730026/issues), and add a new Issue if no one else has requested it.

------

![Demo](./demo.gif)