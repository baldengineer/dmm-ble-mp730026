# 23 F0 04 00 DE 85
# DC voltage -1.502

# 21 F1 04 00 34 02
# Ohms, 056.4


import struct
import numpy as np

def decode_mode_string(data):
	value = ""
	

	return value

def decode_mode_and_range(data):
	mode = data[0]
	mode_string = ""
	range_decimal = data[1]

	value = [hex(mode), mode_string, range_decimal]

	print("	decode_mode: " + str(value))
	# return an int and a string
	return value

def decode_reading_into_hex(data):
	# get the reading nibbles and create a word
	readingMSB = np.int16(data[3])
#	print("5: " + str(hex(readingMSB)))
	readingLSB = np.int16(data[2])
#	print("4: " + str(hex(readingLSB)))
	#shift MSB over and add the LSB, creates a 16-bit word
	value = np.int16((readingMSB << 8) | readingLSB)

	# check if we have a negative value and handle it with bit masking
	if (readingMSB > 0x7F):
		value = readingValue & 0x7FFF
		value = readingValue * -1
	return value

def print_DMM_packet(data):
	#turns the bytearray into tuples, so it is easier to work wh
	unpacked = struct.unpack('>HHBB', data)

	# show what the raw values were, in decimal
	print("Received: ", str(unpacked))

	mode_desc = decode_mode_and_range(unpacked)
	print("mode_desc: " + str(mode_desc[1]))

	readingValue = decode_reading_into_hex(unpacked)

	# print decimal version of reading with zero padding
	## need to determine where the decimal belongs, from mode/range variable
	#readingValue = readingValue / 10
	print(f'Reading: {readingValue:04}')  # needs to be 05 when the decimal comes back
	#print(str(hex(readingValue)) + " " + str(readingValue))


# need to recreate the data we get from bleak
# real bleak-base code does not need this step
#exampleData = [0x23, 0xF0, 0x04, 0x00, 0xDE, 0x85] # DC volts, -1.502 (Negative!!)
exampleData = [0x21, 0xF1, 0x04, 0x00, 0x34, 0x02] # Ohms, 056.4
incomingData = bytearray(exampleData) 
print("incomingData = " + str(incomingData))

print_DMM_packet(incomingData)

