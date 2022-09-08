truck = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>yardbot</title>
  <script src="/rtcbot.js"></script>
  <style>
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
      transform: rotate(-90deg);
      -webkit-transform: rotate(-90deg);
      left: 20px;
    }
    
    .left {
      transform: rotate(90deg);
      -webkit-transform: rotate(90deg);
    }
    

    .down {
      transform: rotate(180deg);
      -webkit-transform: rotate(180deg);
    }
   .centered {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
    body {
      background-image: url("https://www.rv.com/wp-content/uploads/2020/12/IMG_1677.jpg");
      background-size: cover;
      background-repeat: no-repeat;
    }
  </style>
</head>

<body>
    <div class="centered">
      <img id="left" width="100px" src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png" class="ctrl right" />
      <img id="up" width="100px" src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png" class="ctrl up" />
      <img id="down" width="100px" src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png" class="ctrl down" />
      <img id="right" width="100px" src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png" class="ctrl left" />
      <img width="218px" height="100px" src="https://p.kindpng.com/picc/s/107-1078619_stop-sign-icon-png-stop-sign-black-and.png" />      <video autoplay playsinline controls width = "640px" height="480"></video>    
      <button class="ctrl" id="off">off</button>  
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
          if (buttons[i] !== 'off') {
            buttons[i].addEventListener("touchend", sendStopSignal )
          }
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