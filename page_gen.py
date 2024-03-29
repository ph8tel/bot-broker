test = """

<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>yardbot</title>
  <script src="/rtcbot.js"></script>
</head>

<body>

    <video width="320" height="240" controls>
        <source src="movie.mp4" type="video/mp4">
        <source src="movie.ogg" type="video/ogg">
        <source src="movie.webm" type="video/webm">
        <object data="movie.mp4" width="320" height="240">
          <embed src="movie.swf" width="320" height="240">
        </object>
        <button type="button" style="position:absolute; top:50%; left:50%; margin:-40px 0 0 -40px; width:80px; height:80px;" onclick="playPause()">Play/Pause</button>
        <button type="button" style="position:absolute; top:50%; left:10px; margin:-40px 0 0 -40px; width:80px; height:80px;">Mute</button>
        <button type="button" style="position:absolute; top:50%; right:10px; margin:-40px 0 0 -40px; width:80px; height:80px;">Fullscreen</button>
        <button type="button" style="position:absolute; bottom:10px; left:50%; margin:0 0 -40px -40px; width:80px; height:80px;">Captions</button>
      </video>
      
  
  <script>
      var conn = new rtcbot.RTCConnection();
      var sendControlSignal = (cmd) => {
          cmd.preventDefault();
          conn.put_nowait(cmd.target.id)
          }
      var sendStopSignal = (cmd) => conn.put_nowait("stop")

      var buttons = document.getElementsByClassName("ctrl")
      
      if (buttons.length > 0) {
        for (let i = 0; i < buttons.length; i++){
          buttons[i].addEventListener("mousedown", sendControlSignal)
          buttons[i].addEventListener("mouseup", sendStopSignal)
          buttons[i].addEventListener("touchstart", sendControlSignal )
          if (buttons[i] !== 'off') {
            buttons[i].addEventListener("touchend", sendStopSignal )
          }
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
      <img width="218px" height="100px" src="https://p.kindpng.com/picc/s/107-1078619_stop-sign-icon-png-stop-sign-black-and.png" class="ctrl"/>      <video autoplay playsinline controls width = "640px" height="480"></video>    
      <button class="ctrl" id="lightson">flashers</button>  
    </div>
  
  <script>
      var conn = new rtcbot.RTCConnection();
      var sendControlSignal = (cmd) => {
        console.log('sending ', cmd.target.id)
          cmd.preventDefault();
          conn.put_nowait(cmd.target.id)
          }
      var sendStopSignal = (cmd) => conn.put_nowait("stop")

      var buttons = document.getElementsByClassName("ctrl")
      for (let i = 0; i < buttons.length; i++){
          buttons[i].addEventListener("mousedown", sendControlSignal)
          buttons[i].addEventListener("mouseup", sendStopSignal)
          buttons[i].addEventListener("touchstart", sendControlSignal )
          console.log('button ', buttons[i].id)
          if (buttons[i].id !== 'lightson') {
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
controller = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>

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
        <button id="pad-connected">PAD CONNECTED</button>
        <button id="stopped">STOPPED</button>
         <button class="ctrl" id="lightson">flashers</button>  
        </div>
        <video autoplay playsinline controls width = "640px" height="480"></video> <audio autoplay></audio>
      <script>
        const stoppedButton = document.getElementById('stopped')
        const padConnectedButton = document.getElementById('pad-connected')
        const flashersButton = document.getElementById('lightson')
        var conn = new rtcbot.RTCConnection();
          var sendControlSignal = (cmd) => {
            console.log('sending ', cmd.target.id)
              cmd.preventDefault();
              conn.put_nowait(cmd.target.id)
              }
          var sendStopSignal = (cmd) => conn.put_nowait("stop")
    
          var buttons = document.getElementsByClassName("ctrl")
          for (let i = 0; i < buttons.length; i++){
              buttons[i].addEventListener("mousedown", sendControlSignal)
              buttons[i].addEventListener("mouseup", sendStopSignal)
              buttons[i].addEventListener("touchstart", sendControlSignal )
              console.log('button ', buttons[i].id)
              if (buttons[i].id !== 'lightson') {
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
    // if a gamepad exists
    var gamepads = [];
const gpConnected = document.getElementById('pad-connected')
let intervlId
window.stopped = true

let poll_tango = async () => {
    var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
    var gp = gamepads[0]

    for (let i = 0; i < 5; i++) {
        let move = Math.round(gp.axes[i] * 1000)

        if ((Math.abs(move) > 20) && i !== 3) {
            window.stopped = false
            let adjusted = Math.round(1500 + move / 2)
            if (adjusted > 1920) {
                adjusted = 2000
            }
            if (adjusted < 1100) {
                adjusted = 1000
            }
            if (adjusted < 1550 && adjusted > 1450) {
                adjusted = 1500
            }
            if ( sendCommand ) {
                 sendCommand(`axe:${i}:${adjusted}`)
            } else {
                console.log(`axe:${i}:${adjusted}:no send command found`
                )
            }

            console.log(i, adjusted)
        }


    }
}

function gamepadHandler(event, connecting) {
    var gamepad = event.gamepad;
    console.log("Gamepad connected", event)


    gpConnected.style.backgroundColor = 'green'

    //start the show
    intervalId = setInterval(poll_tango, 25)
    // Note:
    // gamepad === navigator.getGamepads()[gamepad.index]

    if (connecting) {
        gamepads.push(gamepad);
    } else {
        gamepads.pop();
    }
}

function GamepadDisconector(event) {
    //cancel interval
    clearInterval(intervalId)
    gamepads.pop()
    gpConnected.style.backgroundColor = 'red'
    gpConnected.innerText = 'PAD NOT CONNECTED'
}

window.addEventListener("gamepadconnected", function (e) { gamepadHandler(e, true); }, false);
window.addEventListener("gamepaddisconnected", function (e) { GamepadDisconector(e); }, false);

      </script>
    
    </body>
    </html>
"""
idx_old = """
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
idx ="""
<!DOCTYPE html>
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="/rtcbot.js"></script>
    <style>
        * {
            box-sizing: border-box;
        }

        .arrow {
            width: 100%;
            border: solid white;
            border-width: 0 3px 3px 0;
            display: inline-block;
            color: #E7E9EB;
        }

        .controll-button {
            width: 100%;
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

        /* Create three equal columns that floats next to each other */
        .column {
            float: left;
            padding: 10px;
        }

        .col-1 {
            width: 15%;
            background-color: #aaa;
            height: 100%;
        }

        .col-2 {
            width: 70%;
        }

        /* Clear floats after the columns */
        .row:after {
            content: "";
            display: table;
            clear: both;
        }
        .centered {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
          }

        /* Responsive layout - makes the three columns stack on top of each other instead of next to each other */
        @media screen and (max-width: 600px) {
            .column {
                width: 100%;
            }
            .arrow {
                width: 50%;
            }
        }
    </style>
    <title>Joe's Yardbot</title>
</head>

<body>
    <div class="row centered">
        <div class="column col-1" >
            <img id="up" width="100px"
                src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png"
                class="ctrl up arrow" />
            <img id="left" width="100px"
                src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png"
                class="ctrl right arrow" />
                <img src="https://p.kindpng.com/picc/s/107-1078619_stop-sign-icon-png-stop-sign-black-and.png" class="ctrl arrow"/>
        </div>
        <div class="column col-2" style="background-color:#bbb;">
            <video autoplay playsinline controls width="100%"></video>
        </div>
        <div class="column col-1">
            <img id="down" width="100px"
            src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png"
            class="ctrl down arrow" />
            <img id="right" width="100px"
                src="https://toppng.com/uploads/preview/wind-direction-png-clipart-library-wind-direction-icon-115629307179jemtlpetx.png"
                class="ctrl left arrow" />
            <img src="data:image/png;base64,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" 
            class="ctrl arrow" id="lightson" /> 
        </div>
    </div>
<script>
    const conn = new rtcbot.RTCConnection();
    const sendControlSignal = (cmd) => {
          cmd.preventDefault();
          conn.put_nowait(cmd.target.id)
          }
    const sendStopSignal = (cmd) => conn.put_nowait("stop")

      const buttons = document.getElementsByClassName("ctrl")
      for (let i = 0; i < buttons.length; i++){
          buttons[i].addEventListener("mousedown", sendControlSignal)
          buttons[i].addEventListener("mouseup", sendStopSignal)
          buttons[i].addEventListener("touchstart", sendControlSignal )
          console.log('button ', buttons[i].id)
          if (buttons[i].id !== 'lightson') {
            buttons[i].addEventListener("touchend", sendStopSignal )
          }
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
</script>
</body>

</html>
        """