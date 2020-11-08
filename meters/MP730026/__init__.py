# Original Author James Lewis 2020-01, Heavily modified into a Class and module by
# Tim 'Geekboy1011" Keller - 2020-06
# Additional major contributions by TisBoyo - 2020-06
# MIT License
# MP730026
# Module to decode and manages instances of a BLE DMM mp730026
import asyncio
import struct
from os import _exit
from re import match as re_match

import numpy as np
from bleak import _logger as bleaklogger
from bleak import BleakClient
from bleak import discover
from bleak import exc
from fastapi import logger as _logger
from txdbus.error import RemoteError  # Used for bluetooth errors

from .. import DMM
from .value_table import values

logger = _logger.logger

debug = False

# This characteristic UUID is for the BDM / MP730026 BLE message
# (do not change this)
CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

# Disable Bleak logging debug spam
if not debug:
    bleaklogger.setLevel(30)  # 30 is logging.WARNING


class MP730026(DMM):
    """
    Connect to a MP730026 Digital Multi-meter.
    Pass the MAC address if known, otherwise autoscan will run.
    """

    def __init__(self, MAC: str = "autoscan", **kwargs):

        # Load the parent class values
        DMM.__init__(self, MAC)

        # Local meter values below here.
        self.MAC = MAC
        self.output_to_console = False
        self.model = "Multicomp Pro MP730026"

        self.__connected = False

        self.obs_scene = kwargs["obs_scene"] if kwargs.get("obs_scene", False) else None
        self.obs_source = kwargs["obs_source"] if kwargs.get("obs_source", False) else None
        if self.obs_scene and self.obs_source:
            from obs import OBS

            self.obs_instance = OBS()
        else:
            self.obs_instance = None

    @property
    def connected(self):
        return self.__connected

    @connected.setter
    def connected(self, connected: bool):

        try:
            # Check if the scene and source have been defined
            if self.obs_scene and self.obs_source:
                # If so, tell OBS to toggle it based on the value
                self.obs_instance.send(connected, self.obs_scene, self.obs_source)
        except AttributeError:
            # Happens on startup because the variables haven't been created yet
            ...

        self.__connected = connected

    async def scan(self):
        logger.warning("Scanning for devices with the name BDM")
        try:
            devices = await discover()
        except RemoteError:
            print("Bluetooth Permissions error. See Readme.md")
            _exit(0)

        for d in devices:
            if d.name == "BDM":  # BDM is the default name of this type of meter
                self.MAC = d.address

        return self.MAC

    def __decode_indicators(self, data: bytearray):
        indicators = data[1]

        hold_indicator_state = bool(indicators & 256)
        rel_indicator_state = bool(indicators & 512)
        auto_range_indicator_state = bool(indicators & 1024)
        low_battery = bool(indicators & 2048)

        return [
            hold_indicator_state,
            rel_indicator_state,
            auto_range_indicator_state,
            low_battery,
        ]

    def __decode_mode_and_range(self, data: bytearray):
        """
        Decodes the Mode and Range from the data bytearray received from the meter
        """

        # First element of the data array is the mode
        mode = data[0]

        try:
            mode_str = self.mode_strings[values[mode][0]]
            units_str = self.unit_strings[values[mode][1]]
            range_decimal_pos = values[mode][2]

        except KeyError:
            # New mode
            mode_str = str(hex(mode))  # its a new mode, so display it
            units_str = "?"
            range_decimal_pos = 5
            logger.error(f"Unknown Values - MP730026.__decode_mode_and_range.mode={hex(mode)}")

        value = [mode, mode_str, units_str, range_decimal_pos]
        logger.debug("	decode_mode: " + str(value))
        logger.debug("decode str: " + str(hex(mode)))

        if units_str == "?":
            logger.debug("Unknown: " + str(hex(mode)))

        return value

    def __decode_reading_into_hex(self, data: tuple, mode_data: list):
        """Decodes the reading into hex format"""

        decimal_position = mode_data[3]

        # get the reading nibbles and create a word
        readingMSB = np.int16(data[3])
        logger.debug("5: " + str(hex(readingMSB)))

        readingLSB = np.int16(data[2])
        logger.debug("4: " + str(hex(readingLSB)))

        # shift MSB over and add the LSB, creates a 16-bit word
        value = np.int16((readingMSB << 8) | readingLSB)

        # did we overload?
        if value < 32676:
            # there is a valid display value
            # check if we have a negative value and handle it with bit masking
            # later in the code, at the negative sign
            if readingMSB > 0x7F:
                value = value & 0x7FFF
            # convert the integer to a string
            final_value = "{:04d}".format(value)

            if decimal_position < 5:
                # only process decimal if valid, 5 isn't a valid position
                final_value = final_value[:decimal_position] + "." + final_value[decimal_position:]
                if readingMSB > 0x7F:
                    final_value = "-" + final_value
                    self.negative = True
                else:
                    self.negative = False
        else:
            # there is not a valid display
            final_value = "O.L"  # TODO The decimal shouldn't be hard coded

        return final_value

    def print_DMM(self):
        """ Send status to logger.info"""

        if debug:
            logger.debug("	mode_desc: " + self.mode)

        string_to_print = f"Reading [{self.mode}]: {self.value} {self.suffix}"

        # is hold on?
        if self.hold:
            string_to_print = string_to_print + ", HOLD"
        if self.rel:
            string_to_print = string_to_print + ", REL"

        return string_to_print

    def parse(self, data: bytearray) -> None:
        """
        Update instance with new data
        """
        try:
            unpacked = struct.unpack(">HHBB", data)
        except struct.error as e:
            # Happens most often when powering off the meter.
            logger.error(e)
            logger.error("If you just powered off the meter, ignore the above error.")
            return None

        # show what the raw values were, in decimal
        logger.debug(f"	Received: {str(unpacked)}")

        mode_range = self.__decode_mode_and_range(unpacked)
        self.hex, self.mode, self.suffix, self.decimal = mode_range

        logger.debug("	mode_desc: " + str(mode_range[2]))

        # Save our values
        self.value = self.__decode_reading_into_hex(unpacked, mode_range)
        (
            self.hold,
            self.rel,
            self.autorange,
            self.low_battery,
        ) = self.__decode_indicators(unpacked)

    def __notification_handler(self, sender: str, data: bytearray):
        self.parse(data)
        if self.output_to_console:
            print(self.print_DMM())

    async def run(self):

        logger.warning(f"{self.model} running as {self.__class__.__name__}.")
        loop = asyncio.get_event_loop()

        # If a MAC was not specified, run autoscan until we find one that matches
        while self.MAC == "autoscan":
            self.MAC = await self.scan()

        logger.warning(f"Connecting to {self.MAC}")
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

                x = await client.is_connected()
                logger.warning(f"Connected: {x}")

                self.connected = True

                await client.start_notify(CHARACTERISTIC_UUID, self.__notification_handler)

                while await client.is_connected():
                    pass

                self.value = False
                self.autorange = False
                self.hold = False
                self.rel = False
                self.decimal = False
                self.suffix = False
                self.connected = False
                logger.warning(f"Disconnected: {x}")
                del client

            except RemoteError:
                print("Bluetooth Permissions error. See Readme.md")
                _exit(0)

            except exc.BleakError:
                continue
