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

# Routes must be imported below settings check because they also import settings
from routes import ws, index


app = FastAPI()

logger = logging.getLogger("app")

# Add routes for FastAPI
app.include_router(ws.router)  # Websocket Routes
app.include_router(index.router)  # Index pages

# Startup event adds the meters to the main asyncio loop
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    for meter in settings.multi_meters:
        loop.create_task(meter.run())

    logger.warning("Ready to connect to the meter...")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=18881, ws="websockets", reload=True)

