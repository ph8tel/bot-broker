from aiohttp import web

routes = web.RouteTableDef()
import os
from rtcbot import Websocket, getRTCBotJS



# Websocket connection to the robot
ws = None


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


@routes.get("/ws")
async def websocket(request):
    global ws
    ws = Websocket(request)
    print("Robot Connected")
    await ws  # Wait until the websocket closes
    print("Robot disconnected")
    return ws.ws


@routes.get("/")
async def index(request):
    return web.Response(
        content_type="text/html",
        text="""
<html>
        <head>
            <title>RTCBot: Remote Video</title>
            <script src="/rtcbot.js"></script>
        </head>
        <body style="text-align: center;padding-top: 30px;">
            <video autoplay playsinline controls width = "100%"></video> <audio autoplay></audio>
            <p>
            </p>
            <button class="ctrl" id="forward">FORWARD</button>
            <button class="ctrl" id="back">BACK</button>
            <button class="ctrl" id="left">LEFT</button>
            <button class="ctrl" id="right">RIGHT</button>
            <input type="text" id="cmd" name = "cmd">
            <script>
                var conn = new rtcbot.RTCConnection();
                const r = document.getElementById("cmd")
                var sendControlSignal = (cmd) => {
                    cmd.preventDefault();
                    conn.put_nowait(cmd.target.id)
                    }
                var sendStopSignal = (cmd) => conn.put_nowait("stop")
                
                var parrot = (e) => {
                    console.log(e.target.id)
                }
                var buttons = document.getElementsByClassName("ctrl")
                console.log(buttons)
                for (let i = 0; i < buttons.length; i++){
                    console.log("adding")
                    buttons[i].addEventListener("mousedown", sendControlSignal)
                    buttons[i].addEventListener("mouseup", sendStopSignal)
                    buttons[i].addEventListener("touchstart", sendControlSignal )
                    buttons[i].addEventListener("touchend", sendStopSignal )

                }
console.log()
                conn.video.subscribe(function(stream) {
                    document.querySelector("video").srcObject = stream;
                });

                async function connect() {
                    let offer = await conn.getLocalDescription();

                    // POST the information to /connect
                    let response = await fetch("/connect", {
                        method: "POST",
                        cache: "no-cache",
                        body: JSON.stringify(offer)
                    });

                    await conn.setRemoteDescription(await response.json());

                    console.log("Ready!");
                }
                connect();

            </script>
        </body>
    </html>
    """,
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

#web.run_app(app, path="0.0.0.0", port=os.environ["PORT"])
web.run_app(app)

