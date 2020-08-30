from datetime import datetime
from json import dumps


class DMM:
    # Used by bleak for the Notify Characteristic of BLE
    NOTIFY_CHARACTERISTIC = "0000fff4-0000-1000-8000-00805f9b34fb"

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
        self.low_battery = False

        self.digits = 4

        self.saved = dict()

    def save(self, name: str = None):
        """Save the current values to the self.saved variable"""

        if not name:
            name = str(datetime.now().timestamp())

        self.saved[name] = self.get_json(save=True)

    def del_all_saved(self):
        """Clear out all of the saved values"""
        self.saved = dict()

    def del_saved_value(self, name: str):
        """Clears a saved value"""
        del self.saved[name]

    def rename_saved(self, name: str, new_name: str):
        """Renames a saved value"""
        self.saved[new_name] = self.saved[name]
        del self.saved[name]

    def get_saved(self):
        """Returns the saved values"""
        return dumps(self.saved)

    def get_json(self, save: bool = False):
        """
        Takes a DMM object and returns the values as a dictionary
        """

        # Create a dictionary of values to be passed to the front end
        values = {
            "timestamp": datetime.now().timestamp(),
            "address": self.address,
            "mode": self.mode,
            "hold": self.hold,
            "rel": self.rel,
            "value": self.value,
            "suffix": self.suffix,
            "decimal": self.decimal,
            "negative": self.negative,
            "autorange": self.autorange,
            "digits": self.digits,
            "connected": self.connected,
            "low_battery": self.low_battery,
        }

        if save:
            values["name"] = datetime.now().timestamp()

        return dumps(values)

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
