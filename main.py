import websockets
import asyncio
import logging
import uvicorn
from os import _exit
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse, HTMLResponse

try:
    import settings
except ModuleNotFoundError:
    print(
        "Settings.py does not exist.\r\n"
        "Copy settings.py.template to settings.py and modify to your settings.",
    )
    _exit(0)

app = FastAPI()

logger = logging.getLogger("app")


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    for meter in settings.multi_meters:
        loop.create_task(meter.run())

    logger.warning("Ready to connect to the meter...")


@app.get("/")
@app.get("/index.html")
async def root():
    # return FileResponse("web/index.html")
    return HTMLResponse(
        '<html><body><center><img src="https://www.inzonedesign.com/wp-content/uploads/2016/10/blog-header-astronaut-houston-we-have-a-problem-im-lost.jpg" /></center></body></html>'
    )


# @app.get("/dmm.js")
# async def send_dmmjs():
#     return FileResponse("web/dmm.js", media_type="text/javascript")


# @app.get("/segment-display.js")
# async def send_segment_displayjs():
#     return FileResponse("web/segment-display.js", media_type="text/javascript")


@app.websocket("/live/{item_id}")
async def send_websocket_live(websocket: WebSocket, item_id: str):
    """Sends meter data to the websocket when connected"""
    await websocket.accept()

    # Defaults to meter 0 if a meter is not passed, or is not a number
    meter_id = int(item_id) if item_id.isdigit() else 0

    # Grab the meter object from the settings file using the index passed
    meter = settings.multi_meters[meter_id]

    while True:

        # Grab a json object of the current meters data
        data = meter.get_json()

        try:
            # Send it to the web socket
            await websocket.send_text(data)

        except websockets.exceptions.WebSocketException:
            # Catch if a client disconnects and ignore it
            # This was done to prevent traceback errors in the console
            pass

        # Send data to the console
        logger.debug(data)

        # We don't need the data at blazing fast speeds, plus it causes websocket errors when sending too fast.
        await asyncio.sleep(0.25)


@app.websocket("/saved/{item_id}")
async def send_websocket_saved(websocket: WebSocket, item_id: str):
    """Sends meter data to the websocket when connected"""
    await websocket.accept()

    # Defaults to meter 0 if a meter is not passed, or is not a number
    meter_id = int(item_id) if item_id.isdigit() else 0

    # Grab the meter object from the settings file using the index passed
    meter = settings.multi_meters[meter_id]

    while True:
        # Grab a json object of the current meters data
        data = meter.get_saved()

        try:
            # Send it to the web socket
            await websocket.send_text(data)

        except websockets.exceptions.WebSocketException:
            # Catch if a client disconnects and ignore it
            # This was done to prevent traceback errors in the console
            pass

        # Send data to the console
        logger.debug(data)

        # We don't need the data at blazing fast speeds, plus it causes websocket errors when sending too fast.
        await asyncio.sleep(0.25)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=18881, ws="websockets", reload=True)

