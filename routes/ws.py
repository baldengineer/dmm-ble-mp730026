from fastapi import APIRouter, WebSocket
import asyncio
import websockets
import logging
import settings  # Meter settings


router = APIRouter()
logger = logging.getLogger("app")


@router.websocket("/live/{item_id}")
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


@router.websocket("/saved/{item_id}")
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
