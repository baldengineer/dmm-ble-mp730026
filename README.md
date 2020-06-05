# dmm-ble-mp730026
 # About 

Python code to access the a Multicomp Pro MP730026 DMM over BLE

This multimeter supports communication over Bluetooth, however, the official software is not very good. It only works with a specific dongle.

Using [the bleak python module](https://github.com/hbldh/bleak), virtually any operation system and bluetooth controller works. So far I have successfully used this code with:

* macOS: Macbook Pro and MacPro (Trashcan)
* Windows 10: Microsoft Surface Book Pro 2
* Linux: Raspberry Pi 3B

The intent for the code is to provide a decoded string from the DMM and to act as an API pass-through for other applications.

decoding dmm maybe.txt are messages from my meter along with descriptions of what the screen showed.



##  Usage

This library exposes a DMM object that exposes all the data for a mp730026 multimeter



```python
  self.MAC = MAC        # Devices MAC address
  self.mode = False     # Current measurement Mode. EG AC voltage
  self.hold = False     # hold Flag
  self.rel = False      # rel Flag
  self.value = False    # String containing 4 digit and one decimal Value 
  self.suffix = False   # String of data suffix. EG mV KΩ
  self.decimal = False  # Decimal Position
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
```



The object also provides a serve_websocket function 

```python
DMM.serve_websocket(websocket)
```

Which is intended to be called from a websockets handler call back to send data to the websocket client until connection close. 

This is provided as an example in run.py



