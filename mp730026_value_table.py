# Created by james lewis (baldengineer) 2020-01
# MIT License
# DMM Decode Byte Array
# Dictionaries of strings for the decoded values

#Establish dictionary of strings
mode_strings = dict(
	dcc = "DC Current",
	acc = "AC Current",
	res = "Resistance",
	cont = "Continuity",
	dcv = "DC Voltage",
	acv = "AC Voltage",
	diode = "Diode",
	freq = "Frequency",
	cap = "Capacitor",
	temp = "Temperature",
	nc = "Non-Contact"
	)

unit_strings = dict(
	uA = "uA",
	mA = "mA",
	A = "A",
	ohm = "Ω",
	kohm = "KΩ",
	mohm = "MΩ",
	mV = "mV",
	V = "V",
	Hz = "Hz",
	KHz = "KHz",
	MHz = "MHz",
	pcnt = "%",
	nF = "nF",
	uF = "uF",
	C = "°C",
	F = "°F",
	space = " "
	)

#Create initial dictionary for values
values = dict()

################################
## DC Current
################################
values[0x90F0] = ['dcc', 'uA', 4]  # DC xxxx uA
values[0x90F1] = ['dcc', 'uA', 3]  # DC xxx.x uA
values[0x97F0] = ['dcc', 'uA', 3]  # DC OL. uA
values[0x99F0] = ['dcc', 'mA', 3]  # xxx.x mA
values[0x9AF0] = ['dcc', 'mA', 2]  # xx.xx mA
values[0xA2F0] = ['dcc', 'A', 2]   # xx.xx A

################################
## AC Current
################################
values[0xD0F0] = ['acc', 'uA', 4]  # AC xxxx uA
values[0xD1F0] = ['acc', 'uA', 3]  # AC xxx.x uA
values[0xD9F0] = ['acc', 'mA', 3]  # AC xxx.x mA
values[0xDAF0] = ['acc', 'mA', 2]  # AC 00.00 mA
values[0xE2F0] = ['acc', 'A', 2]   # AC xx.xx A

################################
## Resistance
################################
values[0x21F1] = ['res', 'ohm', 3]
values[0x22F1] = ['res', 'ohm', 2]  # Ohms xx.xx ohms # unverified
values[0x23F1] = ['res', 'ohm', 1]  # Ohms x.xxx ohms # unverified
values[0x29F1] = ['res', 'kohm', 3] # xxx.x kOhms
values[0x2AF1] = ['res', 'kohm', 2] # xx.xx kOhms
values[0x2BF1] = ['res', 'kohm', 1] # ohms 0.994 kohm
values[0x27F1] = ['res', 'ohm', 3]  #
values[0x21F1] = ['res', 'kohm', 3] #
values[0x2FF1] = ['res', 'mohm', 3] #
values[0x32F1] = ['res', 'mohm', 2] #
values[0x33F1] = ['res', 'mohm', 1] # x.xxx Mohm
values[0x37F1] = ['res', 'mohm', 0] # megaOhms

################################
## Continuity
################################
values[0xE7F2] = ['cont', 'ohm', 4] # OL. cont mode
values[0xE1F2] = ['cont', 'ohm', 3] # xxx.x (?) cont mode

################################
## DC Voltage
################################
values[0x19F0] = ['dcv', 'mV', 3]
values[0x1AF0] = ['dcv', 'mV', 2]   # DC xx.xx mV
values[0x20F0] = ['dcv', 'V', 4]    # DC XXXX V
values[0x21F0] = ['dcv', 'V', 3]    # DC xxx.x V
values[0x22F0] = ['dcv', 'V', 2]    # DC 10 volt
values[0x23F0] = ['dcv', 'V', 1]    # DC 1 Volts

################################
## AC Voltage
################################
values[0x60F0] = ['acv', 'V', 4]    #AC xxxx V
values[0x59F0] = ['acv', 'mV', 3]   #AC xxx.x mV
values[0x5AF0] = ['acv', 'mV', 2]   #AC xx.xx mV
values[0x61F0] = ['acv', 'V', 3]    # AC 000.0 V
values[0x62F0] = ['acv', 'V', 2]    # AC xx.xx V
values[0x63F0] = ['acv', 'V', 1]    #AC x.xxxx V

################################
## Diode
################################
values[0xAEF2] = ['diode', 'V', 0]  # diode
values[0xA3F2] = ['diode', 'V', 1]  # diode x.xxx
values[0xA7F2] = ['diode', 'V', 0]  # diode .OL

################################
## Frequency
################################
values[0xA1F1] = ['freq', 'Hz', 3]  # frequency xxx.x
values[0xA2F1] = ['freq', 'Hz', 2]  # frequency xx.xx
values[0xA3F1] = ['freq', 'Hz', 1]  # frequency x.xx
values[0xA9F1] = ['freq', 'KHz', 3] # frequency xxx.xx
values[0xAAF1] = ['freq', 'KHz', 2] # frequency xx.xx
values[0xABF1] = ['freq', 'KHz', 1] # frequency x.xxx
values[0xB1F1]= ['freq', 'MHz', 3] # frequency xxx.x M # unverified
values[0xB2F1] = ['freq', 'MHz', 2] # frequency xx.xx M # unverified
values[0xB3F1] = ['freq', 'MHz', 1] # frequency x.xxx M
values[0xE1F1] = ['freq', 'pcnt', 3]# Frequency xxx.x %

################################
## Capacitor
################################
values[0x49F1] = ['cap', 'nF', 3] 	# capacitor xxx.x
values[0x4AF1] = ['cap', 'nF', 2]   # capacitor xx.xx nF
values[0x4BF1] = ['cap', 'nF', 1]   # capacitor x.xxx nF # unverified
values[0x51F1] = ['cap', 'uF', 3]   # capacitor xxx.x uF
values[0x52F1] = ['cap', 'uF', 2]   # capacitor xx.xx uF
values[0x53F1] = ['cap', 'uF', 1]   # capacitor x.xxx uF

################################
## Temperature
################################
values[0x20F2] = ['temp', 'C', 4]   # 0000 *C
values[0x60F2] = ['temp', 'F', 4]   # 0000 *F

################################
## NCV
################################
values[0x60F3] = ['nc', 'space', 4]
