import websockets
import asyncio
import json

from mp730026 import DMM


def get_json(meter):
    """
    Takes a DMM object and returns the values as a dictionary
    """

    values = {
        "MAC": meter.MAC,
        "mode": meter.mode,
        "hold": meter.hold,
        "rel": meter.rel,
        "value": meter.value,
        "suffix": meter.suffix,
        "decimal": meter.decimal,
        "negative": meter.negative,
    }

    return json.dumps(values)


async def send_websocket(websocket, path):
    # await BLEDMM.serve_websocket(websocket)
    while True:
        data = get_json(BLEDMM)
        await websocket.send(data)
        print(data)
        await asyncio.sleep(0.25)


print("starting...")
MAC = "A5:B3:C2:25:15:0D"
BLEDMM = DMM(MAC)
websocket_loop = websockets.serve(send_websocket, "0.0.0.0", 18881)

loop = asyncio.get_event_loop()

ble_loop = BLEDMM.run()

loop.run_until_complete(websocket_loop)
loop.run_until_complete(ble_loop)

loop.run_forever()
