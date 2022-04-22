from aiohttp import web

routes = web.RouteTableDef()
import os
from rtcbot import Websocket, getRTCBotJS

import html

# Websocket connection to the robot
ws = None
# Truck Camera Socket
ts = None

# Serve the RTCBot javascript library at /rtcbot.js
@routes.get("/rtcbot.js")
async def rtcbotjs(request):
    return web.Response(content_type="application/javascript", text=getRTCBotJS())


# Called by the browser to set up a connection
@routes.post("/connect")
async def connect(request):
    global ws
    if ws is None:
        raise web.HTTPInternalServerError("There is no robot connected")
    clientOffer = await request.json()

    # Send the offer to the robot, and receive its response
    ws.put_nowait(clientOffer)
    robotResponse = await ws.get()

    return web.json_response(robotResponse)

@routes.post("/connect-truck")
async def connect(request):
    global ts
    if ts is None:
        raise web.HTTPInternalServerError("There is no robot connected")
    clientOffer = await request.json()

    # Send the offer to the robot, and receive its response
    ts.put_nowait(clientOffer)
    robotResponse = await ts.get()

    return web.json_response(robotResponse)
#route for truck
@routes.get("/ts")
async def websocket(request):
    global ts
    ts = Websocket(request)
    print("Truck Connected")
    await ts  # Wait until the websocket closes
    print("Robot disconnected")
    return ts.ws
#route for car
@routes.get("/ws")
async def websocket(request):
    global ws
    ws = Websocket(request)
    print("Robot Connected")
    await ws  # Wait until the websocket closes
    print("Robot disconnected")
    return ws.ws

@routes.get("/truck")
async def index(request):
    return web.Response(
        content_type="text/html",
        text=html.truck,)

@routes.get("/")
async def index(request):
    return web.Response(
        content_type="text/html",
        text=html.controls,
    )


async def cleanup(app=None):
    global ws
    if ws is not None:
        c = ws.close()
        if c is not None:
            await c


app = web.Application()
app.add_routes(routes)
app.on_shutdown.append(cleanup)

web.run_app(app, path="0.0.0.0", port=os.environ["PORT"])
#web.run_app(app)

