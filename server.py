from aiohttp import web
import os
routes = web.RouteTableDef()
from page_gen import idx, truck, test, controller
from rtcbot import Websocket, getRTCBotJS
ws = None # Websocket connection to the robot
ws_blower = None
@routes.get("/ws-blower")
async def websocket_for_blower(request):
    global ws_blower
    ws_blower = Websocket(request)
    print("Robot Connected")
    await ws_blower  # Wait until the websocket closes
    print("Robot disconnected")
    return ws_blower.ws
# Called by the browser to set up a connection
@routes.post("/connect-blower")
async def connect_blower(request):
    global ws_blower
    if ws_blower is None:
        raise web.HTTPInternalServerError("There is no blower connected")
    clientOffer = await request.json()
    print('ws is', clientOffer)
    # Send the offer to the robot, and receive its response
    ws_blower.put_nowait(clientOffer)
    robotResponse = await ws_blower.get()
    return web.json_response(robotResponse)
@routes.get("/ws")
async def websocket(request):
    global ws
    ws = Websocket(request)
    print("Robot Connected")
    await ws  # Wait until the websocket closes
    print("Robot disconnected")
    return ws.ws
@routes.get("/scripts/{filename}")
def get_script(request):
    filename = request.match_info.get('filename')
    return web.FileResponse(os.path.join(os.getcwd(), filename))
@routes.get("/gp")
def get_script(request):
    
    return web.FileResponse(os.path.join(os.getcwd(), 'controller.html'))
@routes.get("/plow")
def get_script(request):
    
    return web.FileResponse(os.path.join(os.getcwd(), 'plowController.html'))
@routes.get("/blower")
def get_script(request):
    
    return web.FileResponse(os.path.join(os.getcwd(), 'blowerController.html'))

@routes.get("/car")
def get_script(request):
    
    return web.FileResponse(os.path.join(os.getcwd(), 'carControllerc.html'))
@routes.get("/test")
def get_test(request):
    return web.FileResponse(os.path.join(os.getcwd(), 'test.html'))

@routes.get("/active")
def get_active(request):
   
    global ws_blower
    global ws
    if ws_blower:
         return web.json_response({"message": "ready", "drone": "car"})
    elif ws:
         return web.json_response({"message": "ready", "drone": "tank"})
    else:
        return web.json_response({"message":"not_ready"})
# Called by the browser to set up a connection
@routes.post("/connect")
async def connect(request):
    global ws
    if ws is None:
        raise web.HTTPInternalServerError("There is no robot connected")
    clientOffer = await request.json()
    print('ws ix', clientOffer)
    # Send the offer to the robot, and receive its response
    ws.put_nowait(clientOffer)
    robotResponse = await ws.get()
    return web.json_response(robotResponse)
@routes.post("/connect-truck")
async def connect_truck(request):
    global ws
    # if ws is None:
    #     raise web.HTTPInternalServerError("There is no robot connected")
    clientOffer = await request.json()
    # Send the offer to the robot, and receive its response
    if ws is None:
        return web.json_response("{ 'bot_available': 'no'}")
    ws.put_nowait(clientOffer)
    robotResponse = await ws.get()
    return web.json_response(robotResponse)
# Serve the RTCBot javascript library at /rtcbot.js
@routes.get("/rtcbot.js")
async def rtcbotjs(request):
    return web.Response(content_type="application/javascript", text=getRTCBotJS())

@routes.get("/")
async def index(request):
    return web.FileResponse(os.path.join(os.getcwd(), 'index.html'))
@routes.get("/tank")
async def tank(request):
    return web.Response(
        content_type="text/html",
        text=controller,)
@routes.get("/test")
async def tank(request):
    return web.Response(
        content_type="text/html",
        text=test,)


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

