# Written by TisBoyo 2020-06
# MIT License
# MP730026
# Module to Test websocket server demo with python and asyncio

import asyncio
import websockets


async def hello():
    uri = "ws://localhost:18881"
    while True:
        async with websockets.connect(uri) as websocket:
            buffer = await websocket.recv()
            print(f"< {buffer}")


asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
