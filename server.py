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
            <title>Joes Yardbot</title>
            <script src="/rtcbot.js"></script>
            <style>
                body {
                  background-color:#E7E9EB;
                }
                #myDIV {
                  width:100%;
                  position:absolute;
                  background-color:#FFFFFF;
                }
                #myDIV div{
                  /* width:100px;
                  height:100px; */
                  width:100%;

                  position:absolute;
                  /* background-color:yellow; */
                  border:1px solid;
                  opacity:0.5;
                  margin:auto;
                }
                #myBox {
                  position:absolute;
                  opacity:1!important;
                  z-index: 0;
                  width:100%;
                }
                .arrow {
                  width: 30px;
                  height: 30px;
                  border: solid black;
                  border-width: 0 3px 3px 0;
                  display: inline-block;
                  padding: 30px;
                  position:absolute;
                  text-color: white;
                }
                
                .right {
                  transform: rotate(-45deg);
                  -webkit-transform: rotate(-45deg);
                }
                
                .left {
                  transform: rotate(135deg);
                  -webkit-transform: rotate(135deg);
                }
                
                .up {
                  transform: rotate(-135deg);
                  -webkit-transform: rotate(-135deg);
                }
                
                .down {
                  transform: rotate(45deg);
                  -webkit-transform: rotate(45deg);
                }
                
                </style>
        </head>
        <body>
            <div id="myDIV">
                <div id="myBox">
            <video autoplay playsinline controls width = "80%"></video> <audio autoplay></audio>
                </div>
            
                    <i id='forward' class="arrow up ctrl" style="top:40px;left:85px;z-index:1;"></i> 
                    <i id='left' class="arrow left ctrl" style="top:100px;left:30px;z-index:1;"></i> 
                    <i id='right'class="arrow right ctrl" style="top:100px;left:180px;z-index:1;"></i> 
                    <i id ="back" class="arrow down ctrl" style="top:220px;left:85px;z-index:1;"></i>  
            </div>


            <script>
                var conn = new rtcbot.RTCConnection();
                var sendControlSignal = (cmd) => {
                    cmd.preventDefault();
                    conn.put_nowait(cmd.target.id)
                    }
                var sendStopSignal = (cmd) => conn.put_nowait("stop")

                var buttons = document.getElementsByClassName("ctrl")
                for (let i = 0; i < buttons.length; i++){
                    buttons[i].addEventListener("mousedown", sendControlSignal)
                    buttons[i].addEventListener("mouseup", sendStopSignal)
                    buttons[i].addEventListener("touchstart", sendControlSignal )
                    buttons[i].addEventListener("touchend", sendStopSignal )
                }

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

web.run_app(app, path="0.0.0.0", port=os.environ["PORT"])
#web.run_app(app)

