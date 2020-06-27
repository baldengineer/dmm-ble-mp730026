import asyncio
from bleak import discover
import time

# Your meter's MAC will probably start with A5:B3:C2...
# and have the name "BDM"
# A5:B3:C2:22:14:D2: BDM


async def scan():
    devices = await discover()
    for d in devices:
        print(d)


if __name__ == "__main__":
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(scan())
        time.sleep(1)
