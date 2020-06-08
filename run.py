import websockets
import asyncio
from mp730026 import DMM


async def send_websocket(websocket, path):
    # await BLEDMM.serve_websocket(websocket)
    while True:
        await websocket.send(BLEDMM.print_DMM())
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
