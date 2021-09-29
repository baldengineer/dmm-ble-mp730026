# Written by TisBoyo 2020-06
# Modifyed by baldengineer 2021-09 
# MIT License
# Open Reflow Controller V2

import logging
import asyncio
import platform
import sys     # call to for exit

from fastapi import logger as _logger

from bleak import BleakClient
from bleak import _logger as bleaklogger
from bleak import exc
from bleak import discover

from .. import DMM

from re import match as re_match
from txdbus.error import RemoteError  # Used for bluetooth errors

logger = _logger.logging

debug = False

# This characteristic UUID is for the BDM / MP730026 BLE message
# (do not change this)
CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# Disable Bleak logging debug spam
if not debug:
	bleaklogger.setLevel(30)  # 30 is logging.WARNING


class openvapors(DMM):

	def __init__(self, MAC: str = "88:25:83:F2:7A:D2"):
		# Load the parent class values
		DMM.__init__(self, MAC)

		# Local meter values below here.
		self.MAC = MAC
		self.output_to_console = False
		self.model = "Open Vapors Reflow"

	def print_DMM(self):
		""" Send status to logger.info"""

		if debug:
			logger.debug("  mode_desc: " + self.mode)

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

		reflow_string = data.decode("UTF-8").strip()

		try:
			reflow_string_fields = reflow_string.split(",")

		except:
			# should probably handle these
			# but I think this just means the reflow oven
			# returned BLE Disconnected
			return None

		# show what the raw values were, in decimal
		logger.debug(f" Received: {str(reflow_string)}")

		# Save our values
		self.value = reflow_string_fields[1]

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
				logger.warning(f"Disconnected: {x}")
				del client

			except RemoteError:
				print("Bluetooth Permissions error. See Readme.md")
				_exit(0)

			except exc.BleakError:
				continue