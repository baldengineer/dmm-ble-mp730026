import websockets
import asyncio
import json
import datetime

from mp730026 import DMM

# Set the MAC address of the MP730026 meter here.
MAC = "A5:B3:C2:25:15:0D"


def get_json(meter):
    """
    Takes a DMM object and returns the values as a dictionary
    """

    # Create a dictionary of values to be passed to the front end
    values = {
        "timestamp": datetime.datetime.now().timestamp(),
        "MAC": meter.MAC,
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
        data = get_json(BLEDMM)
        try:
            # Send it to the web socket
            await websocket.send(data)
        except websockets.exceptions.ConnectionClosedOK:
            # Catch if a client disconnects and ignore it
            # This was done to prevent traceback errors in the console
            pass

        # Send data to the console
        print(data)
        # We don't need the data at blazing fast speeds, plus it causes websocket errors when sending too fast.
        await asyncio.sleep(0.25)


print("Ready to connect to the meter...")

# Create the  mp730026 object
BLEDMM = DMM(MAC)

# Setup our websocket loop
websocket_loop = websockets.serve(send_websocket, "0.0.0.0", 18881)

# Create our async loop
loop = asyncio.get_event_loop()

# Setup our meter loop
ble_loop = BLEDMM.run()

# Run all of our loops
loop.run_until_complete(websocket_loop)
loop.run_until_complete(ble_loop)
# forever
loop.run_forever()
