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
        <title>Joe's Yardbot</title>
        <script src="/rtcbot.js"></script>
        <style>
            #page {
      display: grid;
      width: 100%;
      height: 250px;
      grid-template-areas: "head head"
                           "nav  main"
                           "nav  foot";
      grid-template-rows: 50px 1fr 30px;
      grid-template-columns: 150px 1fr;
    }
    
    #page > header {
      grid-area: head;
      background-color: #8ca0ff;
    }
    
    #page > nav {
      grid-area: nav;
      background-color: #ffa08c;
    }
    
    #page > main {
      grid-area: main;
      background-color: #ffff64;
    }
    
    #page > footer {
      grid-area: foot;
      background-color: #8cffa0;
    }
       .slider.round {
      border-radius: 34px;
    }
    
    .slider.round:before {
      border-radius: 50%;
    }
    /* The switch - the box around the slider */
    .switch {
      position: relative;
      display: inline-block;
      width: 100%;
      height: 100%;
    }
    
    /* Hide default HTML checkbox */
    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    .background {
      height: 100px;
      width: 100%;
    }
    
    /* The slider */
    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ccc;
      -webkit-transition: .4s;
      transition: .4s;
    }
    
    .slider:before {
      position: absolute;
      content: "";
      height: 26px;
      width: 26px;
      left: 4px;
      bottom: 4px;
      background-color: white;
      -webkit-transition: .4s;
      transition: .4s;
    }
    
    input:checked + .slider {
      background-color: #2196F3;
    }
    
    input:focus + .slider {
      box-shadow: 0 0 1px #2196F3;
    }
    
    input:checked + .slider:before {
      -webkit-transform: translateX(26px);
      -ms-transform: translateX(26px);
      transform: translateX(26px);
    }
        </style>
    </head>
    <body><section id="page">
        <header>Header</header>
        <nav> 
            <div class="background">
            <label class="switch" >
            <input type="checkbox" >
            <span class="slider round" id="a"></span>
          </label>
          </div>
          <div class="background">
            <label class="switch">
            <input type="checkbox">
            <span class="slider round" id ="b"></span>
          </label>
          </div>
          <div class="background">
            <label class="switch">
            <input type="checkbox">
            <span class="slider round" id = "c"></span>
          </label>
          </div>
          <div class="background">
            <label class="switch" >
            <input type="checkbox" >
            <span class="slider round" id = "d"></span>
          </label>
          </div>
          <div class="background">
            <label class="switch" >
            <input type="checkbox">
            <span class="slider round"  id = "e"></span>
          </label>
          </div>
          <div class="background">
            <label class="switch" >>
            <span class="slider round" id ="f">
            <input type="checkbox" ></span>
          </label>
          </div></nav>
        <main>
            <video autoplay playsinline controls width="100%"></video> <audio autoplay></audio>
        </main>
        <footer><button class="switch" id="left">LEFT</button>
          <button class="switch" id="right">RIGHT</button>
          <button class="switch" id="forward">FORWARD</button>
          <button class="switch" id="left">BACK</button>
        </footer>
      </section>
        <p>
       
        </p>
        <script>
            var conn = new rtcbot.RTCConnection();

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
        <script>
            const socket = new WebSocket('wss://yardbots.herokuapp.com/');
        
        // Connection opened
        socket.addEventListener('open', function (event) {
            socket.send('Hello Server!');
        });
            var process_touchstart = (e) => {
                socket.send(e.srcElement.id)
                console.log(e.srcElement.id,e, " sent")
                 
            }
            var process_touchend = (e) => {
              socket.send("stop")
              console.log("sent stop command")
            }
            var switches = document.getElementsByClassName("switch")
        for (var i=0; i < switches.length; i++) {
            switches[i].addEventListener('touchstart', process_touchstart, false);
            switches[i].addEventListener('touchend', process_touchend, false);
        
        }
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
# web.run_app(app)

