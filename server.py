from aiohttp import web
import os
routes = web.RouteTableDef()
from page_gen import idx, truck, test, controller
from rtcbot import Websocket, getRTCBotJS
ws = None # Websocket connection to the robot
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
    
    return web.FileResponse(os.path.join(os.getcwd(), 'ploaController.html'))
@routes.get("/blower")
def get_script(request):
    
    return web.FileResponse(os.path.join(os.getcwd(), 'snowBlower.html'))

@routes.get("/car")
def get_script(request):
    
    return web.FileResponse(os.path.join(os.getcwd(), 'carControllerc.html'))

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
    return web.Response(
        content_type="text/html",
        text=idx,)
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

