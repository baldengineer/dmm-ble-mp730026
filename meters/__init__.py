
class DMM:
    def __init__(self, address):
        self.address = address
        self.mode = False
        self.hold = False
        self.rel = False
        self.value = False
        self.suffix = False
        self.decimal = False
        self.negative = False
        self.autorange = False
        self.connected = False

    # Establish dictionary of strings
    mode_strings = dict(
        dcc="DC Current",
        acc="AC Current",
        res="Resistance",
        cont="Continuity",
        dcv="DC Voltage",
        acv="AC Voltage",
        diode="Diode",
        freq="Frequency",
        cap="Capacitor",
        temp="Temperature",
        nc="Non-Contact",
    )

    unit_strings = dict(
        uA="uA",
        mA="mA",
        A="A",
        ohm="Ω",
        kohm="KΩ",
        mohm="MΩ",
        mV="mV",
        V="V",
        Hz="Hz",
        KHz="KHz",
        MHz="MHz",
        pcnt="%",
        nF="nF",
        uF="uF",
        C="°C",
        F="°F",
        space=" ",
    )