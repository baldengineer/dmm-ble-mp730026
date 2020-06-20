# Written by TisBoyo 2020-06
# MIT License
# MP730026
# Module to Mimic instances of a BLE DMM mp730026 causing random display variations
import asyncio
import random
from .. import DMM


class Demo(DMM):
    def __init__(self, address: str = "Demo"):
        # Load the parent class values
        DMM.__init__(self, address)

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

            _, self.suffix = random.choice(list(self.unit_strings.items()))

            await asyncio.sleep(1)
