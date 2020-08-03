from fastapi import APIRouter, WebSocket, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
import uvicorn
import asyncio
import websockets
import logging
import settings  # Meter settings


router = APIRouter()
logger = logging.getLogger("app")

# Default colors that are passed when using the redirects
default_oncolor = "rgb(250,250,164,.9)"
default_offcolor = "rgb(16,32,16,.5)"
default_background = "rgb(0,0,0,.5)"
default_text = "%20"


@router.get("/")
async def root(request: Request):
    response = f"""
    <html>
    <body>
    """

    count = 0
    for meter in settings.multi_meters:
        response += f'<a href="{request.base_url}{count}">ID: {count} - {meter.model} - {meter.address} - Connected: {meter.connected}</a><br />'
        count += 1

    response += f"""
    </body>
    </html>
    """
    return HTMLResponse(response)


# Favicon just because
@router.get("/favicon.ico")
async def favicon():
    return FileResponse("web/favicon.ico")


@router.get("/dmm.js")
async def send_dmmjs():
    return FileResponse("web/dmm.js", media_type="text/javascript")


@router.get("/segment-display.js")
async def send_segment_displayjs():
    return FileResponse("web/segment-display.js", media_type="text/javascript")


# The actual route to load the meter
@router.get("/meter")
async def meter():
    return FileResponse("web/meter.html", media_type="text/html")


# Route to load saved data
@router.get("/saved")
async def saved():
    return FileResponse("web/saved.html", media_type="text/html")


# A redirect to access live data based on meter id
@router.get("/{item_id}")
async def live_meter(
    item_id: str,
    request: Request,
    offcolor: str = default_offcolor,
    oncolor: str = default_oncolor,
    background: str = default_background,
    text: str = default_text,
):
    url = (
        f"{request.base_url}meter?"
        f"websocketserver={request.base_url.hostname}"
        f"&websocketport={request.base_url.port}"
        f"&meter={item_id}"
        f"&onColor={oncolor}"
        f"&offColor={offcolor}"
        f"&background={background}"
        f"&displaytxt={text}"
    )

    return RedirectResponse(url)


# A redirect to access saved data based on meter id
@router.get("/saved/{item_id}")
async def saved_meter(
    item_id: str,
    request: Request,
    offcolor: str = default_offcolor,
    oncolor: str = default_oncolor,
    background: str = default_background,
    text: str = default_text,
):
    url = (
        f"{request.base_url}saved"
        f"?websocketserver={request.base_url.hostname}"
        f"&websocketport={request.base_url.port}"
        f"&meter={item_id}"
        f"&oncolor={oncolor}"
        f"&offcolor={offcolor}"
        f"&background={background}"
        f"&displaytxt={text}"
    )
    return RedirectResponse(url)
