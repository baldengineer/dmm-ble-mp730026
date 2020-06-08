# dmm-ble-mp730026

 # About

Python code to access the a Multicomp Pro MP730026 DMM over BLE

This multimeter supports communication over Bluetooth, however, the official software is not very good. It only works with a specific dongle.

Using [the bleak python module](https://github.com/hbldh/bleak), virtually any operation system and bluetooth controller works. So far I have successfully used this code with:

* macOS: Macbook Pro and MacPro (Trashcan)
* Windows 10: Microsoft Surface Book Pro 2
* Linux: Raspberry Pi 3B

The intent for the code is to provide an object representing the DMM. 

decoding dmm maybe.txt are messages from my meter along with descriptions of what the screen showed.

bleak_scan.py can be used to find the MAC address of your meter.



##  Usage

This library exposes a DMM object that exposes all the data for a mp730026 multimeter



```python
  self.MAC = MAC         # Devices MAC address
  self.mode = False      # Current measurement Mode. EG AC voltage
  self.hold = False      # hold Flag
  self.rel = False       # rel Flag
  self.value = False     # String containing 4 digit and one decimal Value
  self.suffix = False    # String of data suffix. EG mV KΩ
  self.decimal = False   # Decimal Position
  self.negative = False  # If the number is a negative value
  self.autorange = False # Auto-range flag
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





# Included Example

Included is an example for connecting a meter to a web-socket for sending the data across the internet, In this case to a web page to show off the multimeter reading in real time. 

executing: 

```
run.py
```

Will start up the websocket and bluetooth services for getting data from the meter.

### Accessing

Opening index.html either locally or hosted with the following flags

###### websocketserver *required

IP Address or Host name of server, eg 127.0.0.1, 192,168.1.100, raspberrypi

###### websocketport *required

Web socket port, default is 18881

###### background

RGB syntax or [HTML color names](https://htmlcolorcodes.com/color-names/),

```
rgb(250,128,114)
salmon
```



###### oncolor

Color of the darker background elements of the display

###### offcolor

Color of the brighter foreground elements



##### Examples

- /index.html?websocketserver=127.0.0.1&websockport=18881&background=grey&onColor=black&offColor=dimgrey
- /index.html?websocketserver=127.0.0.1&websockport=18881&background=black&onColor=Lime&offColor=DarkGreen



### OBS Browser Source

This was actually designed to be used with OBS as a browser source. The url you generated above goes in URL

height and width are as follows

```
width = 250
height = 85
```

All other defaults are fine. 


### Raspberry Pi specifics

Permissions for the Pi user to access bluetooth are needed

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