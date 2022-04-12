from aiohttp import web

routes = web.RouteTableDef()
import os
from rtcbot import Websocket, getRTCBotJS



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
                video{
                    position: absolute;
                    z-index: 0;
                }
                .arrow {
                    opacity: 60%;
                  width: 30px;
                  height: 30px;
                  border: solid white;
                  border-width: 0 3px 3px 0;
                  display: inline-block;
                  padding: 30px;
                  position:absolute;
                  color: #E7E9EB;
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
            <video autoplay playsinline controls width = "640px" height="480"></video> <audio autoplay></audio>
                </div>
            
                    <i id='forward' class="arrow up ctrl" style="top:40px;left:95px;z-index:1;"></i> 
                    <i id='left' class="arrow left ctrl" style="top:120px;left:20px;z-index:1;"></i> 
                    <i id='right'class="arrow right ctrl" style="top:120px;left:170px;z-index:1;"></i> 
                    <i id ="back" class="arrow down ctrl" style="top:200px;left:95px;z-index:1;"></i>  
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
                    let response = await fetch("/connect-truck", {
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
        """,)

@routes.get("/")
async def index(request):
    return web.Response(
        content_type="text/html",
        text="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yardbot</title>
    <style>
        *,
*:before,
*:after {
  box-sizing: border-box;
}

body {
  background: #fff;
}

div {
  padding: 0;
  margin: 0;
  width: 3em;
  height: 3em;
  position: absolute;
}

.wrapper {
  /* position: absolute; */
  height: 9em;
  /* margin: auto; */
  top: 100px;
  bottom: 0;
  left: 100px;
  right: 0;
  filter: drop-shadow(7px 5px 5px #777);
  float:right;

}

.center {
  /* z-index: 2; */
  top: 3em;
}

.center-circle {
  position: static;
/*   background: #222532; */
  background: #777;
/*   background: #90E4FF; */
/*   background: #7FFFB5; */
  border-radius: 100%;
  margin: auto;
  width: 75%;
  height: 75%;
  z-index: 3;
}

.up,
.right,
.down,
.left,
.center {
  display: flex;
  background: #000;
  padding: 12px;
  border: 1px solid #222;
/*   background: #51D6FF; */
/*   background: #37FF8B; */
}

.right {
  top: 3em;
  left: 3em;
}

.left {
  top: 3em;
  right: 3em;
}

.down {
  top: 6em;
}

.up-triangle {
  position: absolute;
  bottom: 16px;
  right: 8px;
  margin: auto;
  width: 65%;
  height: 65%;
  border-left: solid 15px transparent; 
  border-right: solid 15px transparent; 
  border-bottom: solid 20px #777; 
}

.right-triangle {
  position: absolute;
  bottom: 8px;
  right: 0px;
  margin: auto;
  width: 65%;
  height: 65%;
  border-left: solid 15px transparent; 
  border-right: solid 15px transparent; 
  border-bottom: solid 20px #777;
  transform: rotate(90deg);
}

.down-triangle {
  position: absolute;
  bottom: 0px;
  right: 8px;
  margin: auto;
  width: 65%;
  height: 65%;
  border-left: solid 15px transparent; 
  border-right: solid 15px transparent; 
  border-bottom: solid 20px #777;
  transform: rotate(180deg);
}

.left-triangle {
  position: absolute;
  bottom: 8px;
  left: 1px;
  margin: auto;
  width: 65%;
  height: 65%;
  border-left: solid 15px transparent; 
  border-right: solid 15px transparent; 
  border-bottom: solid 20px #777;
  transform: rotate(-90deg);
}
screen {
    display: flex;
}
vid {
    flex: 82%;
}
dpad {
    flex: 18%;
}

    </style>
</head>
<body>
    <screen>
    <dpad>
                <div class="wrapper">

        <div class="center">
            <div class="center-circle"></div>
        </div>
        
        <div class="up direction" >
          <div class="up-triangle" id="forward"></div>
        </div>
      
        <div class="right direction" >
          <div class="right-triangle" id="right"></div>
        
        </div>

        
        <div class="down direction" >
          <div class="down-triangle" id="back"></div>
        </div>
      
        <div class="left direction" >
          <div class="left-triangle" id="left"></div>
        </div>
</div>
</dpad>
<vid>
<video autoplay playsinline controls width="100%" ></video> <audio autoplay></audio>

</vid>
</screen>

        
<script>
    var conn = new rtcbot.RTCConnection();
    var sendControlSignal = (cmd) => {
                cmd.preventDefault();
                console.log(cmd.target.id)
                conn.put_nowait(cmd.target.id)
                }
            var sendStopSignal = (cmd) => conn.put_nowait("stop")

            var buttons = document.getElementsByClassName("direction")
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

