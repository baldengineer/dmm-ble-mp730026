#!/usr/bin/python

# Created by james lewis (baldengineer) 2020-01
# MIT License
# test_dmm_decode
# Script to test the decoder mp730026_decode_bytearray.py

from mp730026_decode_bytearray import print_DMM_packet
import asyncio

debug = False

# need to recreate the data we get from bleak
# real bleak-base code does not need this step
#exampleData = [0x23, 0xF0, 0x04, 0x00, 0xDE, 0x85] # DC volts, -1.502 (Negative!!)
#exampleData = [0x21, 0xF1, 0x04, 0x00, 0x34, 0x02] # Ohms, 056.4
#exampleData = [0x23, 0xF0, 0x04, 0x00, 0xE6, 0x0C] # DC Volts, 3.302
#exampleData = [0x22, 0xF0, 0x04, 0x00, 0x7E, 0x04] # DC Volts, 11.50
#exampleData = [0x19, 0xF0, 0x04, 0x00, 0x41, 0x14] # mV, 518.5 mV

exampleArray = [[0x23, 0xF0, 0x04, 0x00, 0xDE, 0x85], [0x21, 0xF1, 0x04, 0x00, 0x34, 0x02],[0x23, 0xF0, 0x04, 0x00, 0xE6, 0x0C],[0x22, 0xF0, 0x04, 0x00, 0x7E, 0x04],[0x19, 0xF0, 0x04, 0x00, 0x41, 0x14]]

async def main():
	for exampleData in exampleArray:
		incomingData = bytearray(exampleData) 
		if (debug): print("incomingData = " + str(incomingData))

		await print_DMM_packet(incomingData)

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	task = loop.create_task(main())
	loop.run_until_complete(task)
