import asyncio
from bleak import discover
import time

# Your meter's MAC will probably start with A5:B3:C2...
# and have the name "BDM"
# A5:B3:C2:22:14:D2: BDM

async def run():
    devices = await discover()
    for d in devices:
        print(d)

while(1):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	time.sleep(1)