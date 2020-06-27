from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import websockets
import logging
import settings  # Meter settings


router = APIRouter()
logger = logging.getLogger("app")


@router.get("/")
@router.get("/index.html")
async def root():
    # return FileResponse("web/index.html")
    return HTMLResponse(
        '<html><body><center><img src="https://www.inzonedesign.com/wp-content/uploads/2016/10/blog-header-astronaut-houston-we-have-a-problem-im-lost.jpg" /></center></body></html>'
    )


# @router.get("/dmm.js")
# async def send_dmmjs():
#     return FileResponse("web/dmm.js", media_type="text/javascript")


# @router.get("/segment-display.js")
# async def send_segment_displayjs():
#     return FileResponse("web/segment-display.js", media_type="text/javascript")
