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
    <title>login</title>
    <style>
        @import url('https://fonts.googleapis.com/css?family=Poppins');

/* BASIC */

html {
  background-color: #56baed;
}

body {
  font-family: "Poppins", sans-serif;
  height: 100vh;
}

a {
  color: #92badd;
  display:inline-block;
  text-decoration: none;
  font-weight: 400;
}

h2 {
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  text-transform: uppercase;
  display:inline-block;
  margin: 40px 8px 10px 8px; 
  color: #cccccc;
}



/* STRUCTURE */

.wrapper {
  display: flex;
  align-items: center;
  flex-direction: column; 
  justify-content: center;
  width: 100%;
  min-height: 100%;
  padding: 20px;
}

#formContent {
  -webkit-border-radius: 10px 10px 10px 10px;
  border-radius: 10px 10px 10px 10px;
  background: #fff;
  padding: 30px;
  width: 90%;
  height: 600px;
  /* max-width: 450px; */
  position: relative;
  padding: 0px;
  -webkit-box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
  box-shadow: 0 30px 60px 0 rgba(0,0,0,0.3);
  text-align: center;
}

#formFooter {
  background-color: #f6f6f6;
  border-top: 1px solid #dce8f1;
  padding: 25px;
  text-align: center;
  -webkit-border-radius: 0 0 10px 10px;
  border-radius: 0 0 10px 10px;
}



/* TABS */

h2.inactive {
  color: #cccccc;
}

h2.active {
  color: #0d0d0d;
  border-bottom: 2px solid #5fbae9;
}



/* FORM TYPOGRAPHY*/

input[type=button], input[type=submit], input[type=reset]  {
  background-color: #56baed;
  border: none;
  color: white;
  padding: 15px 80px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  text-transform: uppercase;
  font-size: 13px;
  -webkit-box-shadow: 0 10px 30px 0 rgba(95,186,233,0.4);
  box-shadow: 0 10px 30px 0 rgba(95,186,233,0.4);
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
  margin: 5px 20px 40px 20px;
  -webkit-transition: all 0.3s ease-in-out;
  -moz-transition: all 0.3s ease-in-out;
  -ms-transition: all 0.3s ease-in-out;
  -o-transition: all 0.3s ease-in-out;
  transition: all 0.3s ease-in-out;
}

input[type=button]:hover, input[type=submit]:hover, input[type=reset]:hover  {
  background-color: #39ace7;
}

input[type=button]:active, input[type=submit]:active, input[type=reset]:active  {
  -moz-transform: scale(0.95);
  -webkit-transform: scale(0.95);
  -o-transform: scale(0.95);
  -ms-transform: scale(0.95);
  transform: scale(0.95);
}
input[type=password] {
  background-color: #f6f6f6;
  border: none;
  color: #0d0d0d;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 5px;
  width: 85%;
  border: 2px solid #f6f6f6;
  -webkit-transition: all 0.5s ease-in-out;
  -moz-transition: all 0.5s ease-in-out;
  -ms-transition: all 0.5s ease-in-out;
  -o-transition: all 0.5s ease-in-out;
  transition: all 0.5s ease-in-out;
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
}
input[type=text]  {
  background-color: #f6f6f6;
  border: none;
  color: #0d0d0d;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 5px;
  width: 85%;
  border: 2px solid #f6f6f6;
  -webkit-transition: all 0.5s ease-in-out;
  -moz-transition: all 0.5s ease-in-out;
  -ms-transition: all 0.5s ease-in-out;
  -o-transition: all 0.5s ease-in-out;
  transition: all 0.5s ease-in-out;
  -webkit-border-radius: 5px 5px 5px 5px;
  border-radius: 5px 5px 5px 5px;
}
input[type=password]:focus {
  background-color: #fff;
  border-bottom: 2px solid #5fbae9;

}
input[type=text]:focus {
  background-color: #fff;
  border-bottom: 2px solid #5fbae9;
}

input[type=text]:placeholder {
  color: #cccccc;
}

input[type=password]:placeholder {
  color: #cccccc;
}

/* ANIMATIONS */

/* Simple CSS3 Fade-in-down Animation */
.fadeInDown {
  -webkit-animation-name: fadeInDown;
  animation-name: fadeInDown;
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

@-webkit-keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

/* Simple CSS3 Fade-in Animation */
@-webkit-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@-moz-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }

.fadeIn {
  opacity:0;
  -webkit-animation:fadeIn ease-in 1;
  -moz-animation:fadeIn ease-in 1;
  animation:fadeIn ease-in 1;

  -webkit-animation-fill-mode:forwards;
  -moz-animation-fill-mode:forwards;
  animation-fill-mode:forwards;

  -webkit-animation-duration:1s;
  -moz-animation-duration:1s;
  animation-duration:1s;
}

.fadeIn.first {
  -webkit-animation-delay: 0.4s;
  -moz-animation-delay: 0.4s;
  animation-delay: 0.4s;
}

.fadeIn.second {
  -webkit-animation-delay: 0.6s;
  -moz-animation-delay: 0.6s;
  animation-delay: 0.6s;
}

.fadeIn.third {
  -webkit-animation-delay: 0.8s;
  -moz-animation-delay: 0.8s;
  animation-delay: 0.8s;
}

.fadeIn.fourth {
  -webkit-animation-delay: 1s;
  -moz-animation-delay: 1s;
  animation-delay: 1s;
}

/* Simple CSS3 Fade-in Animation */
.underlineHover:after {
  display: block;
  left: 0;
  bottom: -10px;
  width: 0;
  height: 2px;
  background-color: #56baed;
  content: "";
  transition: width 0.2s;
}

.underlineHover:hover {
  color: #0d0d0d;
}

.underlineHover:hover:after{
  width: 100%;
}



/* OTHERS */

*:focus {
    outline: none;
} 

#icon {
  width:60%;
}

* {
  box-sizing: border-box;
}

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

.wrapper2 {
  /* position: absolute; */
  height: 9em;
  /* margin: auto; */
  top: 150px;
  /* bottom: 0; */
  left: 80px;
  /* right: 0; */
  filter: drop-shadow(7px 5px 5px #777);
  /* float:right; */

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
video {
    width: 640px;
    height: 480px;
}
.screen {
    margin: auto;
    width: 66%;
    padding: 10px;

}
    </style>
    <script src="/rtcbot.js"></script>

</head>
<body>

<div class="wrapper fadeInDown">
    <div id="formContent">
    <status>Bot not conected</status>
    <screen>
        <dpad>
            <div class="wrapper2">
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
        <button id = "off"> off</button>
        <vid>
                <video autoplay playsinline controls ></video> <audio autoplay></audio>
        </vid>
    </screen>
      
    </div>
    </div>
    <script>
        var stats = document.querySelector("status")
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
                              let streams = await navigator.mediaDevices.getUserMedia({audio: true, video: false});
                conn.audio.putSubscription(streams.getAudioTracks()[0])
                let offer = await conn.getLocalDescription();

                // POST the information to /connect
                let response = await fetch("/connect", {
                    method: "POST",
                    cache: "no-cache",
                    body: JSON.stringify(offer)
                });
<<<<<<< HEAD
                conn.subscribe( (msg) => {
                  console.log("here", msg, msg == '"bot_ready"')
                  if ( msg === '"bot_ready"') {
                    console.log("bot is ready")
                    stats.innerHTML = '<p>Bot is Ready!</p>'
                    }
                  })
    conn.audio.subscribe(function(stream) {
  document.querySelector("audio").srcObject = stream;
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
=======

                await conn.setRemoteDescription(await response.json());

                console.log("Ready!");
            }
            connect();

        </script>
>>>>>>> b39de5fbf97257c1f22bb697d74c7357aa4e5e23
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

