from fastapi import APIRouter, WebSocket, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
import uvicorn
import asyncio
import websockets
import logging
import settings  # Meter settings


router = APIRouter()
logger = logging.getLogger("app")


@router.get("/")
@router.get("/index.html")
async def root():
    return HTMLResponse(
        '<html><body><center><img src="https://www.inzonedesign.com/wp-content/uploads/2016/10/blog-header-astronaut-houston-we-have-a-problem-im-lost.jpg" /></center></body></html>'
    )


@router.get("/favicon.ico")
async def favicon():
    return FileResponse("web/favicon.ico")


@router.get("/dmm.js")
async def send_dmmjs():
    return FileResponse("web/dmm.js", media_type="text/javascript")


@router.get("/segment-display.js")
async def send_segment_displayjs():
    return FileResponse("web/segment-display.js", media_type="text/javascript")


@router.get("/meter")
async def meter():
    return FileResponse("web/meter.html", media_type="text/html")


@router.get("/saved")
async def saved():
    return FileResponse("web/saved.html", media_type="text/html")


@router.get("/{item_id}")
async def live_meter(item_id: str, request: Request):
    url = f"{request.base_url}meter?websocketserver={request.base_url.hostname}&websocketport={request.base_url.port}&meter={item_id}"
    return RedirectResponse(url)


@router.get("/saved/{item_id}")
async def saved_meter(item_id: str, request: Request):
    url = f"{request.base_url}saved?websocketserver={request.base_url.hostname}&websocketport={request.base_url.port}&meter={item_id}"
    return RedirectResponse(url)
