from fastapi import APIRouter, WebSocket
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


@router.get("/meter.html")
async def meter():
    return FileResponse("web/meter.html", media_type="text/html")


@router.get("/{item_id}")
async def live_meter(item_id: str):
    # url = f"http://192.168.1.71:18881/meter.html?websocketserver=192.168.1.71&websocketport=18881&meter={item_id}"
    # return RedirectResponse(url)
    pass
