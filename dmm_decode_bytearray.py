# Created by james lewis (baldengineer) 2020-01
# MIT License
# DMM Decode Byte Array
# Module to decode the byte stream from a MP730026 DMM

import struct
import numpy as np

debug = False

def decode_mode_and_range(data):
	mode = data[0]
	mode_string = "???"
	range_decimal_pos = 5


################################
## Current
################################

	if (mode == 0x99F0):
		#xxx.x mA
		mode_string = "mA"
		range_decimal_pos = 3

	if (mode == 0x9AF0):
		# xx.xx mA
		mode_string = "mA"
		range_decimal_pos = 2

	if (mode == 0x9BF0):
		# unverified
		# x.xxx mA
		mode_string = "mA"
		range_decimal_pos = 1


################################
## Resistance
################################

	if (mode == 0x21f1):
		# Ohms xxx.x ohms
		mode_string = "ohms"
		range_decimal_pos = 3

	if (mode == 0x22f1):
		# unverified
		# Ohms xx.xx ohms
		mode_string = "ohms"
		range_decimal_pos = 2

	if (mode == 0x23f1):
		# unverified
		# Ohms x.xxx ohms
		mode_string = "ohms"
		range_decimal_pos = 1


	if (mode == 0x29F1):
		# xxx.x kOhms
		mode_string = "Kohms"
		range_decimal_pos = 3

	if (mode == 0x2AF1):
		# xx.xx kOhms
		mode_string = "Kohms"
		range_decimal_pos = 2
	
	if (mode == 0x2BF1):
		# ohms 0.994 kohm
		mode_string = "Kohms"
		range_decimal_pos = 1



	if (mode == 0x37F1):
		# megaOhms
		mode_string = "Mohm"
		range_decimal_pos = 0


################################
## Continuity
################################
	if (mode == 0xE7F2):
		# OL. cont mode
		mode_string = "Cont"
		range_decimal_pos = 4

	if (mode == 0xE1F2):
		# xxx.x (?) cont mode
		mode_string = "Cont"
		range_decimal_pos = 3

################################
## Voltage
################################
	if (mode == 0x19f0):
		# mV
		mode_string = "mV"
		range_decimal_pos = 3

	if (mode == 0x22f0):
		# DC 10 volt
		mode_string = "V"
		range_decimal_pos = 2

	if (mode == 0x23f0):
		# DC 1 Volts
		mode_string = "V"
		range_decimal_pos = 1




################################
## Diode
################################
	if (mode == 0xAEF2):
		# diode
		mode_string = "diode"
		range_decimal_pos = 0

	if (mode == 0xA3f2):
		# diode x.xxx
		mode_string = "diode"
		range_decimal_pos = 1

	if (mode == 0xA7F2):
		# diode .OL
		mode_string = "diode"
		range_decimal_pos = 0

################################
## Frequency
################################
	if (mode == 0xA1F1):
		# frequency xxx.x
		mode_string = "Hz"
		range_decimal_pos = 3

	if (mode == 0xA2F1):
		# frequency xx.xx
		mode_string = "Hz"
		range_decimal_pos = 2

	if (mode == 0xA3F1):
		# frequency x.xx
		mode_string = "Hz"
		range_decimal_pos = 1


	if (mode == 0xA9F1):
		# frequency xxx.xx
		mode_string = "KHz"
		range_decimal_pos = 3

	if (mode == 0xAAF1):
		# frequency xx.xx
		mode_string = "KHz"
		range_decimal_pos = 2

	if (mode == 0xABF1):
		# frequency x.xxx
		mode_string = "KHz"
		range_decimal_pos = 1


	if (mode == 0xB13F1):
		# unverified
		# frequency xxx.x M
		mode_string = "MHz"
		range_decimal_pos = 3

	if (mode == 0xB2F1):
		# unverified
		# frequency xx.xx M
		mode_string = "MHz"
		range_decimal_pos = 2

	if (mode == 0xB3F1):
		# frequency x.xxx M
		mode_string = "MHz"
		range_decimal_pos = 1

################################
## Capacitor
################################		
	if (mode == 0x49F1):
		# capacitor xxx.x
		mode_string	 = "nF"
		range_decimal_pos = 3

	if (mode == 0x4AF1):
		# capacitor xx.xx nF
		mode_string = "nF"
		range_decimal_pos = 2

	if (mode == 0x4BF1):
		# unverified
		# capacitor x.xxx nF
		mode_string = "nF"
		range_decimal_pos = 1


	if (mode == 0x51F1):
		# capacitor xxx.x uF
		mode_string = "uF"
		range_decimal_pos = 3

	if (mode == 0x52F1):
		# capacitor xx.xx uF
		mode_string = "uF"
		range_decimal_pos = 2

	if (mode == 0x53F1):
		# capacitor x.xxx uF
		mode_string = "uF"
		range_decimal_pos = 1


	value = [hex(mode), mode_string, range_decimal_pos]

	if (debug): print("	decode_mode: " + str(value))
	#print("decode str: " + str(hex(mode)))

	if (mode_string == "???"):
		print("Unknown: " + str(hex(mode)))

	# return an int and a string
	return value

def decode_reading_into_hex(data, decimal_position):
	# get the reading nibbles and create a word
	readingMSB = np.int16(data[3])
#	print("5: " + str(hex(readingMSB)))
	readingLSB = np.int16(data[2])
#	print("4: " + str(hex(readingLSB)))
	#shift MSB over and add the LSB, creates a 16-bit word
	value = np.int16((readingMSB << 8) | readingLSB)

	# did we overload?
	if (value < 32676):
		# there is a valid display value
		# check if we have a negative value and handle it with bit masking
		# later in the code, at the negative sign
		if (readingMSB > 0x7F): value = value & 0x7FFF
	

		#convert the integer to a string
		final_value = "{:04d}".format(value)
		
		if (decimal_position < 5):
			# only process decimal if valid, 5 isn't a valid position
			final_value = final_value[:decimal_position] + "." + final_value[decimal_position:]
			if (readingMSB > 0x7F): final_value = "-" + final_value
	else:
		# there is not a valid display
		final_value = "O.L" #TODO The decimal shouldn't be hard coded


	return final_value

def print_DMM_packet(data):
	#turns the bytearray into tuples, so it is easier to work wh
	unpacked = struct.unpack('>HHBB', data)

	# show what the raw values were, in decimal
	if (debug): print("	Received: ", str(unpacked))

	mode_desc = decode_mode_and_range(unpacked)
	
	if (debug): print("	mode_desc: " + str(mode_desc[1]))
	# mode_desc[2] contains the range multiplier 
	readingValue = (decode_reading_into_hex(unpacked, mode_desc[2]))

	# print decimal version of reading with zero padding
	## need to determine where the decimal belongs, formatm mode/range variable
	#readingValue = readingValue / 10
	#print(f'Reading: {readingValue:04}')  # needs to be 05 when the decimal comes back
	print("Reading: " + readingValue + " " + mode_desc[1])
	#print(str(hex(readingValue)) + " " + str(readingValue))


