import asyncio
from rtcbot import Websocket, RTCConnection, PiCamera
# from chassis import Tank
import time
from PCA9685 import PCA9685
import time
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

Pos0 = 1500
Pos1 = 1500
pwm.setServoPulse(0, 1500)  # throttle nuetral
pwm.setServoPulse(1, 1500)  # steering middle
pwm.setServoPulse(4, 500)  # lights off
pwm.setServoPulse(2, 2500)  # plow up

cam = PiCamera()
conn = RTCConnection()
conn.video.putSubscription(cam)

# Connect establishes a websocket connection to the server,
# and uses it to send and receive info to establish webRTC connection.


async def connect():
    ws = Websocket("https://bot-broker.herokuapp.com/ws")
    # ws = Websocket("http://192.168.0.13:8080/ws")
# asynd def connect():
    # global ws
    print("waiting")

    msg = await ws.get()
    robotDescription = await conn.getLocalDescription(msg)
    ws.put_nowait(robotDescription)
    print("Started WebRTC")
    await ws.close()


def controller_movement(moves):
    servo_to_move = abs(int(moves[1]) - 1)
    print('move', moves[2], servo_to_move)
    pwm.setServoPulse(servo_to_move, int(moves[2]))


async def cmnd():
    while True:
      msg = await conn.get()
      print("got", msg)
      command_packet = msg.split(':')
      if command_packet[0] == 'servo':
         pwm.setServoPulse(int(command_packet[1]), int(command_packet[2]))
      if command_packet[0] == 'button':

        if command_packet[1] == "stop":
          pwm.setServoPulse(0, 1500)
          pwm.setServoPulse(1, 1500)
        elif command_packet[1] == "lights":
          print('lights setting')
          pwm.setServoPulse(4, 500)
          time.sleep(.1)
          pwm.setServoPulse(4, 2500)
        if command_packet[1] == "plow":
            if command_packet[2] == 'up':
               pwm.setServoPulse(2, 2500)
            if command_packet[2] == 'down':
              pwm.setservoPulse(2, 500)
      
         

        
      #await ws.close()
    

asyncio.ensure_future(connect())
asyncio.ensure_future(cmnd())
try:
    asyncio.get_event_loop().run_forever()
finally:
    cam.close()
    conn.close()



