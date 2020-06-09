# Original Author James Lewis 2020-01, Heavily modified into a Class and module by
# Tim 'Geekboy1011" Keller - 2020-06
# Additional major contributions by TisBoyo - 2020-06
# MIT License
# MP730026
# Module to decode and manages instances of a BLE DMM mp730026
import struct
import numpy as np
from bleak import BleakClient
from bleak import _logger as logger
from bleak import exc
import asyncio


from value_table import values, mode_strings, unit_strings

debug = False

# This characteristic UUID is for the BDM / MP730026 BLE message
# (do not change this)
CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"


class DMM:
    def __init__(self, MAC):
        self.MAC = MAC
        self.mode = False
        self.hold = False
        self.rel = False
        self.value = False
        self.suffix = False
        self.decimal = False
        self.negative = False
        self.autorange = False
        self.connected = False

    def __decode_hold_and_rel(self, data):
        rel_indicator_state = False
        hold_indicator_state = False
        auto_range_indicator_state = False
        indicators = data[1]

        # probably a better way to do this with masking, but don't wanna
        if indicators == 256:
            hold_indicator_state = True
        elif indicators == 512:
            rel_indicator_state = True
        elif indicators == 768:
            hold_indicator_state = True
            rel_indicator_state = True
        elif indicators == 1024:
            auto_range_indicator_state = True
        elif indicators == 1280:
            auto_range_indicator_state = True
            hold_indicator_state = True

        return [hold_indicator_state, rel_indicator_state, auto_range_indicator_state]

    def __decode_mode_and_range(self, data):
        mode = data[0]

        try:
            mode_str = mode_strings[values[mode][0]]
            units_str = unit_strings[values[mode][1]]
            range_decimal_pos = values[mode][2]

        except KeyError:
            # New mode
            mode_str = str(hex(mode))  # its a new mode, so display it
            units_str = "?"
            range_decimal_pos = 5

        value = [mode, mode_str, units_str, range_decimal_pos]
        # if (debug): print("	decode_mode: " + str(value))
        # print("decode str: " + str(hex(mode)))

        # 	if (units_str == "?"):
        # 		print("Unknown: " + str(hex(mode)))

        # return an int and a string

        return value

    def __decode_reading_into_hex(self, data, mode_data):
        decimal_position = mode_data[3]

        # get the reading nibbles and create a word
        readingMSB = np.int16(data[3])
        # 	print("5: " + str(hex(readingMSB)))
        readingLSB = np.int16(data[2])
        # 	print("4: " + str(hex(readingLSB)))
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
                final_value = (
                    final_value[:decimal_position]
                    + "."
                    + final_value[decimal_position:]
                )
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
        """ Print state to STDOUT """

        if debug:
            print("	mode_desc: " + self.mode)
        string_to_print = "Reading [{}]: {} {}".format(
            self.mode, self.value, self.suffix
        )

        # is hold on?
        if self.hold:
            string_to_print = string_to_print + ", HOLD"
        if self.rel:
            string_to_print = string_to_print + ", REL"
        print(string_to_print)
        return string_to_print

    def parse(self, data):
        """ Update Instance with new data"""
        unpacked = struct.unpack(">HHBB", data)

        # show what the raw values were, in decimal
        if debug:
            print("	Received: ", str(unpacked))

        mode_range = self.__decode_mode_and_range(unpacked)
        self.hex, self.mode, self.suffix, self.decimal = mode_range

        if debug:
            print("	mode_desc: " + str(mode_range[2]))
        self.value = self.__decode_reading_into_hex(unpacked, mode_range)

        # is hold on?
        # hold_and_rel = decode_hold_and_rel(unpacked)
        self.hold, self.rel, self.autorange = self.__decode_hold_and_rel(unpacked)

    def __notification_handler(self, sender, data, debug=False):
        self.parse(data)

    async def run(self):

        loop = asyncio.get_event_loop()

        # client = BleakClient(self.MAC, loop=loop)

        while True:
            client = BleakClient(self.MAC, loop=loop)

            try:
                while not await client.connect():
                    pass

                x = await client.is_connected()
                logger.info("Connected: {0}".format(x))

                self.connected = True

                await client.start_notify(
                    CHARACTERISTIC_UUID, self.__notification_handler
                )

                while await client.is_connected():
                    pass

                self.value = False
                self.autorange = False
                self.hold = False
                self.rel = False
                self.decimal = False
                self.suffix = False
                self.connected = False
                del client

            except exc.BleakError:
                continue
