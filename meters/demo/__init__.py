# Written by TisBoyo 2020-06
# MIT License
# MP730026
# Module to Mimic instances of a BLE DMM mp730026 causing random display variations
import asyncio
import random
from fastapi import logger as _logger
from .. import DMM

logger = _logger.logging


class Demo(DMM):
    def __init__(self, address: str = "Demo"):
        # Load the parent class values
        DMM.__init__(self, address)

        self.model = "Demo Display"

    async def run(self):

        logger.warning("Demo Meter running.")
        self.decimal = 0
        self.connected = True

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

            _, self.suffix = random.choice(list(self.unit_strings.items()))

            # Fake some saved data
            self.save()

            # Wipe out the dummy saved data when we get to 10 values
            if len(self.saved) >= 10:
                self.saved = dict()

            await asyncio.sleep(1)
