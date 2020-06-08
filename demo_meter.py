# Original Author James Lewis 2020-01, Heavily modified into a Class and module by
# Tim 'Geekboy1011" Keller - 2020-06
# MIT License
# MP730026
# Module to decode and manages instances of a BLE DMM mp730026
import asyncio
import random

from value_table import values, mode_strings, unit_strings


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

    async def run(self):

        self.decimal = 0
        while True:

            self.value = str(random.randint(0, 9999)).zfill(4)

            if self.decimal >= 0 and self.decimal < 4:
                self.decimal += 1
            elif self.decimal >= 4:
                self.decimal = 0

            self.negative = random.choice([True, False])
            self.hold = random.choice([True, False])
            self.rel = random.choice([True, False])
            self.autorange = random.choice([True, False])

            _, self.suffix = random.choice(list(unit_strings.items()))

            await asyncio.sleep(1)
