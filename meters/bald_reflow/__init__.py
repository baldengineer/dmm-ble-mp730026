# Written by Tisboyo - 2020-08
# Used to display Baldengineer Reflow oven controller on stream
# MIT License

import asyncio
import struct
import numpy as np
from os import _exit
from re import match as re_match
from collections import namedtuple

from bleak import BleakClient
from bleak import _logger as logger
from bleak import exc
from bleak import discover
from txdbus.error import RemoteError  # Used for bluetooth errors

from .. import DMM


class BaldReflow(DMM):
    """
    Connect to BaldEngineers Reflow Oven controller
    """

    def __init__(self, MAC: str = "autoscan"):
        # Load the parent class values
        DMM.__init__(self, MAC)

        # Local meter values below here.
        self.MAC = MAC

    async def scan(self):
        logger.warning(f"Scanning for devices with the name BaldReflow")
        try:
            devices = await discover()
        except RemoteError:
            print("Bluetooth Permissions error. See Readme.md")
            _exit(0)

        for d in devices:
            if d.name == "BaldReflow":
                self.MAC = d.address

        return self.MAC

    def __decode_settings(self, data: bytearray) -> namedtuple:
        settings = data[0]

        # Create named tuple to return values
        nt = namedtuple("Settings", ["mode", "suffix"])

        # Process the recieved data
        mode = "temp"
        suffix = "C"

        value = nt(mode, suffix)

        return value

    def __decode_value(self, data: bytearray) -> int:
        value = data[1]

        # Process the recieved data

        return value

    def parse(self, data: bytearray) -> None:
        unpacked = struct.unpack(">HH", data)

        settings = self.__decode_settings(unpacked)
        value = self.__decode_value(unpacked)

        self.mode = settings.mode
        self.suffix = settings.suffix
        self.value = value

    def __notification_handler(self, sender: str, data: bytearray) -> None:
        self.parse(data)

    async def run(self) -> None:

        # Grab the async loop
        loop = asyncio.get_event_loop()

        # If a MAC was not specified, run autoscan until we find one that matches
        while self.MAC == "autoscan":
            self.MAC = await self.scan()

        logger.warning(f"Connecting to BaldReflow-{self.MAC}")

        while True:
            try:
                if re_match("^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$", self.MAC):
                    client = BleakClient(self.MAC, loop=loop)
                else:
                    raise ValueError

            except TypeError:
                logger.error("Invalid data type passed for MAC")
                break
            except ValueError:
                logger.error("Invalid MAC address")
                break

            try:
                while not await client.connect():
                    pass

                conn = await client.is_connected()
                logger.warning(f"Connected: {conn}")

                self.connected = True

                await client.start_notify(
                    DMM.NOTIFY_CHARACTERISTIC, self.__notification_handler
                )

                while await client.is_connected():
                    # Just hang out here and wait while the meter is connected.
                    # This allows the notification to run when updates are recieved
                    # but also do cleanup when it disconnects.
                    pass

                self.value = False
                self.connected = False
                logger.warning(f"Disconnected: {conn}")

                del client

            except RemoteError:
                print("Bluetooth Permissions error. See Readme.md")
                _exit(0)

            except exc.BleakError:
                continue

