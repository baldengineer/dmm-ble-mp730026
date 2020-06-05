import websockets
import asyncio
from mp730026 import DMM

async def m(websocket,path):
    await DLEDMM.serve_websocket(websocket)
    
BLEDMM = DMM(MAC)
server_loop = websockets.serve(m, "127.0.0.1", 18881)
loop = asyncio.get_event_loop()
loop.run_until_complete(server_loop)
loop.run_forever()