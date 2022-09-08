truck = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Joe's Yardbot</title>
  <script src="/rtcbot.js"></script>
  <style>
    body {
      background: #fff;
      font: 16px/1 Arial, Helvetica, sans-serif;
      padding: 0;
      margin: 0;
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
    .grid-container {
      display: grid;
      grid-template-columns: auto auto;
      grid-template-rows: auto auto;
      grid-column-gap: 10px;
      grid-row-gap: 10px;
      background: #fff;
      padding: 5px;
    }

    .grid-item {
      background: rgba(255, 255, 255, 0.8);
      border: 1px solid rgba(0, 0, 0, 0.8);
      padding: 5px;
      font-size: 12px;
      text-align: center;
    }
  </style>
</head>

<body>

<h1>Joe's Yardbot</h1>

<div class="grid-container">
  <div class="grid-item">            
    <div id="myDIV">
        <div id="myBox">
         <video autoplay playsinline controls width = "640px" height="480"></video> <audio autoplay></audio>
        </div>
    </div>
   </div>  
    <div class="grid-item">
    <div style="background-color: black;">
        <i id='forward' class="arrow up ctrl" ></i> 
        <i id='left' class="arrow left ctrl" ></i> 
        <i id='right'class="arrow right ctrl" ></i> 
        <i id ="back" class="arrow down ctrl" ></i>
        <button class="ctrl" id="off">off</button>  
    </div>
  </div>

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
"""
idx = """
<html>
    <head>
        <title>RTCBot: Remote Video</title>
        <script src="/rtcbot.js"></script>
    </head>
    <body style="text-align: center;padding-top: 30px;">
        <button id="stop">stop</button>
        <video autoplay playsinline controls></video>
        
        <p>
        Open the browser's developer tools to see console messages (CTRL+SHIFT+C)
        </p>
        <script>
            var conn = new rtcbot.RTCConnection();

            conn.video.subscribe(function(stream) {
                document.querySelector("video").srcObject = stream;
            });
            async function connect() {
                let streams = await navigator.mediaDevices.getUserMedia({audio: false, video: false});


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
    """