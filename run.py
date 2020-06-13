import websockets
import asyncio
import json
import datetime
import logging

import settings

# from meters.MP730026 import MP730026 as DMM

# from meters.demo import Demo as DMM

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)


def get_json(meter):
    """
    Takes a DMM object and returns the values as a dictionary
    """

    # Create a dictionary of values to be passed to the front end
    values = {
        "timestamp": datetime.datetime.now().timestamp(),
        "address": meter.address,
        "mode": meter.mode,
        "hold": meter.hold,
        "rel": meter.rel,
        "value": meter.value,
        "suffix": meter.suffix,
        "decimal": meter.decimal,
        "negative": meter.negative,
        "autorange": meter.autorange,
    }

    return json.dumps(values)


async def send_websocket(websocket, path):
    """Sends meter data to the websocket when connected"""
    while True:

        # Grab a json object of the current data
        # if path == "/test":
        #     data = get_json(TESTDMM)
        # else:
        data = get_json(settings.multi_meters[0])

        try:
            # Send it to the web socket
            await websocket.send(data)
        except websockets.exceptions.ConnectionClosedOK:
            # Catch if a client disconnects and ignore it
            # This was done to prevent traceback errors in the console
            pass

        # Send data to the console
        logger.debug(data)

        # We don't need the data at blazing fast speeds, plus it causes websocket errors when sending too fast.
        await asyncio.sleep(0.25)


if __name__ == "__main__":
    print("Ready to connect to the meter...")

    # Setup our websocket loop
    websocket_loop = websockets.serve(send_websocket, "0.0.0.0", 18881)

    # Create our async loop
    loop = asyncio.get_event_loop()

    # Run all of our loops
    loop.run_until_complete(websocket_loop)

    # Load all of the meters that are in settings into the loop
    for meter in settings.multi_meters:
        loop.create_task(meter.run())

    # forever
    loop.run_forever()
