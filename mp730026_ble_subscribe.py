#!/usr/bin/python

# Modified by james lewis (@baldengineer)
# MIT License
# 2020
# Script to connect to Multicomp Pro MP730026 by BLE with the Bleak Module
# Based on bleak example
# Requires mpp730026_decode_bytearray.py to be in the same directory

import logging
import asyncio
import platform
from mp730026_decode_bytearray import print_DMM_packet

from bleak import BleakClient
from bleak import _logger as logger

# Change this to your meter's address
address = ("A5:B3:C2:24:15:16") # for Windows and Linux
#address = ("4DA7C422-D3DE-4AE5-AF14-CFEBDD3B85D1") # for macOS

# This characteristic UUID is for the BDM / MP730026 BLE message
# (do not change this)
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
        await asyncio.sleep(460.0, loop=loop)
        await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, False))
