# dmm-ble-mp730026
 Python code to access the a Multicomp Pro MP730026 DMM over BLE

This multimeter supports communication over Bluetooth, however, the included software is not very good. And it only works with a specific dongle.

Using [the bleak python module](https://github.com/hbldh/bleak), virtually any operation system and bluetooth controller works. So far I have successfully used this code with:

* macOS: Macbook Pro and MacPro (Trashcan)
* Windows 10: Microsoft Surface Book Pro 2
* Linux: Raspberry Pi 3B

The intent for the code is to provide a decoded string from the DMM and to act as an API pass-through for other applications.

decoding dmm maybe.txt are messages from my meter along with descriptions of what the screen showed.