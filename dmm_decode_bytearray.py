# Created by james lewis (baldengineer) 2020-01
# MIT License
# DMM Decode Byte Array
# Module to decode the byte stream from a MP730026 DMM
#
# Heads-up, This code contains bugs
#
# TODO
# Overload on resistance is probably scaled wrong
# hard to capture values

import struct
import numpy as np
from values import values, mode_strings, unit_strings

debug = False

def decode_hold_and_rel(data):
	rel_indicator_state = False
	hold_indicator_state = False
	indicators = data[1]

	#probably a better way to do this with masking, but don't wanna
	if (indicators == 256): hold_indicator_state = True
	if (indicators == 512): rel_indicator_state = True
	if (indicators == 768):
		hold_indicator_state = True
		rel_indicator_state = True

	return [hold_indicator_state, rel_indicator_state]

def decode_mode_and_range(data):
	mode = data[0]

	try:
		mode_str = mode_strings[values[mode][0]]
		units_str = unit_strings[values[mode][1]]
		range_decimal_pos = values[mode][2]

	except KeyError:
		#New mode
		mode_str = str(hex(mode)) # its a new mode, so display it
		units_str = "?"
		range_decimal_pos = 5

	value = [mode, mode_str, units_str, range_decimal_pos]
	#if (debug): print("	decode_mode: " + str(value))
	#print("decode str: " + str(hex(mode)))

#	if (units_str == "?"):
#		print("Unknown: " + str(hex(mode)))

	# return an int and a string
	return value

def decode_reading_into_hex(data, mode_data):
	decimal_position = mode_data[3]

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

	if (debug): print("	mode_desc: " + str(mode_desc[2]))
	readingValue = (decode_reading_into_hex(unpacked, mode_desc))

	string_to_print = "Reading [" + mode_desc[1] + "]: " + readingValue + " " + mode_desc[2]

	# is hold on?
	#hold_and_rel = decode_hold_and_rel(unpacked)
	if (decode_hold_and_rel(unpacked)[0] == True): string_to_print = string_to_print + ", HOLD"
	if (decode_hold_and_rel(unpacked)[1] == True): string_to_print = string_to_print + ", REL"
	print(string_to_print)

	#print("Reading [", end='')
	#print(mode_desc[1], end='')
	#print("]: ", end='')
	#print(readingValue, end='')
	#print(" ", end='')
	#print(mode_desc[2])

	#print(str(hex(readingValue)) + " " + str(readingValue))


