import websockets
import asyncio
import logging
import signal
from os import _exit

try:
    import settings
except ModuleNotFoundError:
    print(
        "Settings.py does not exist.\r\n"
        "Copy settings.py.template to settings.py and modify to your settings.",
    )
    _exit(0)


logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    print("\r\nProgram exited successfully.")
    _exit(0)


async def send_websocket(websocket, path):
    """Sends meter data to the websocket when connected"""
    while True:

        # Index 0 will always be "", a blank index will exist after trailing slash
        path_values = path.split("/")

        # Defaults to meter 0 if a meter is not passed, or is not a number
        meter_id = int(path_values[1]) if path_values[1].isdigit() else 0

        # Returns saved data if index 2 is "saved", path=/0/saved or path=//saved
        get_saved = (
            True
            if (len(path_values) > 2 and path_values[2].startswith("saved"))
            else False
        )

        # Grab the meter object from the settings file using the index passed
        meter = settings.multi_meters[meter_id]

        if get_saved:
            # Grab the saved data for the meter
            data = meter.get_saved()

        else:
            # Grab a json object of the current meters data
            data = meter.get_json()

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
    signal.signal(signal.SIGINT, signal_handler)

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
