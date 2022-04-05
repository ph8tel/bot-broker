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
            }
            .arrow {
              border: solid black;
              border-width: 0 3px 3px 0;
              display: inline-block;
              padding: 3px;
              position:absolute;
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
            .arrow {
                margin:auto;
            }
            </style>
    </head>
    <body>
        <div id="myDIV">
            <div id="myBox">
        <video autoplay playsinline controls width = "100%"></video> <audio autoplay></audio>
            </div>
        
                <button class="arrow up ctrl" style="top:40px;left:55px;z-index:1;"></i> 
                <button class="arrow left ctrl" style="top:60px;left:30px;z-index:1;"></button> 
                <button class="arrow right ctrl" style="top:60px;left:80px;z-index:1;"></button> 
                <button class="arrow down ctrl" style="top:80px;left:55px;z-index:1;"></button>  
        </div>
        <p id="gamepad-info">Waiting for Gamepad.</p>
        
        <div id="ball"></div>

        <script>
            var conn = new rtcbot.RTCConnection();
            //gamepad

            var gamepadInfo = document.getElementById("gamepad-info");
var ball = document.getElementById("ball");
var start;
var a = 0;
var b = 0;

var rAF = window.mozRequestAnimationFrame ||
window.webkitRequestAnimationFrame ||
window.requestAnimationFrame;

var rAFStop = window.mozCancelRequestAnimationFrame ||
window.webkitCancelRequestAnimationFrame ||
window.cancelRequestAnimationFrame;

window.addEventListener("gamepadconnected", function() {
var gp = navigator.getGamepads()[0];
gamepadInfo.innerHTML = "Gamepad connected at index " + gp.index + ": " + gp.id + ". It has " + gp.buttons.length + " buttons and " + gp.axes.length + " axes.";

gameLoop();
});

window.addEventListener("gamepaddisconnected", function() {
gamepadInfo.innerHTML = "Waiting for gamepad.";

rAFStop(start);
});

if(!('GamepadEvent' in window)) {
// No gamepad events available, poll instead.
var interval = setInterval(pollGamepads, 500);
}

function pollGamepads() {
var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
for (var i = 0; i < gamepads.length; i++) {
var gp = gamepads[i];
if(gp) {
  //gamepadInfo.innerHTML = "Gamepad connected at index " + gp.index + ": " + gp.id + ". It has " + gp.buttons.length + " buttons and " + gp.axes.length + " axes.";
  gameLoop();
  clearInterval(interval);
}
}
}

function buttonPressed(b) {
if (typeof(b) == "object") {
return b.pressed;
}
return b == 1.0;
}
var speed = 1500
var steer = 1500
function gameLoop() {
var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
if (!gamepads)
return;

var gp = gamepads[0];
if (buttonPressed(gp.buttons[7])) {
b+=gp.buttons[7].value;
let rounded = Math.round(gp.buttons[7].value * 1000)
speed = 1500 + rounded
if (speed > 1800){
    speed = 1800
}
//console.log(speed) 
} else if (buttonPressed(gp.buttons[6])) {
b-= gp.buttons[6].value
let rounded = Math.round(gp.buttons[6].value * 1000)
// console.log(rounded)
speed = 1500 - rounded
console.log(speed)
if (speed < 700){
    speed = 700
}
} else {
  speed = 1500
}
if  (gp.axes[2] > .001) {
  //console.log(gp.axes[2])
  a+= gp.axes[2]
  let rounded = Math.round(gp.axes[2] * -500)
  steer += rounded
  if (steer < 600){
    steer = 600
  }
} else if  (gp.axes[2] < -.001) {
  //console.log(gp.axes[2])
  a+= gp.axes[2]
  let rounded = Math.round(gp.axes[2] * -500)
  steer += rounded
  if (steer > 2400){
    steer = 2400
  }
} else {
  steer = 1500
}
console.log(speed,steer)
conn.put_nowait(speed+":"+steer)


// ball.style.left = a*2 + "px";
// ball.style.top = b*2 + "px";

var start = rAF(gameLoop);
};
//end gamepad
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

