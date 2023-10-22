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
