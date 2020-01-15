#!/usr/bin/python

# Created by james lewis (baldengineer)
# MIT License
# Bleak_Service_Subscribe (TODO: Rename)
# Script to connect to Multicomp Pro MP730026 by BLE with the Bleak Module

import logging
import asyncio
import platform
from dmm_decode_bytearray import print_DMM_packet

from bleak import BleakClient
from bleak import _logger as logger

#CHARACTERISTIC_UUID = "00001800-0000-1000-8000-00805f9b34fb" #Generic Access Profile
#CHARACTERISTIC_UUID = "00001801-0000-1000-8000-00805f9b34fb" #Generic Attribute Profile
#CHARACTERISTIC_UUID = "0000180a-0000-1000-8000-00805f9b34fb" #Device Information
#CHARACTERISTIC_UUID = "0000fff0-0000-1000-8000-00805f9b34fb" #Vendor specific
#CHARACTERISTIC_UUID = "00010203-0405-0607-0809-0a0b0c0d1911" #Unknown
 

CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"


def notification_handler(sender, data, debug=False):
    """Simple notification handler which prints the data received."""
    #print("{0}: {1}".format(sender, data))
    if (debug): print("Handling...")
    if (debug): print("Data is " + str(type(data)))
    

    array = bytearray(data)
    
    if (debug): print(str(sender) + " : ", end="")
    if (debug): 
        for arr in array:
            print(hex(arr))
        print("")
    if (debug): print("... done handling")
    print_DMM_packet(array)

async def run(address, loop, debug=False):
    if debug:
        import sys

        # loop.set_debug(True)
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(60.0, loop=loop)
        await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        "A5:B3:C2:22:14:D2"  # <--- Change to your device's address here if you are using Windows or Linux
       # if platform.system() != "Darwin"
       # else "243E23AE-4A99-406C-B317-18F1BD7B4CBE"  # <--- Change to your device's address here if you are using macOS
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, False))
