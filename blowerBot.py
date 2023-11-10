import asyncio
from rtcbot import Websocket, RTCConnection, PiCamera
#from chassis import Tank

from PCA9685 import PCA9685
import time 
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

Pos0 = 1500  
Pos1 = 1500 
pwm.setServoPulse(0, 1500) #direction
pwm.setServoPulse(1, 1500) #steering
pwm.setServoPulse(2, 1500)  #pan
pwm.setServoPulse(3, 1500) #tilt
pwm.setServoPulse(4, 500) #lights
pwm.setServoPulse(5, 1000) #blower

cam = PiCamera()
conn = RTCConnection()
conn.video.putSubscription(cam)

# Connect establishes a websocket connection to the server,
# and uses it to send and receive info to establish webRTC connection.
async def connect():
    ws = Websocket("https://bot-broker.herokuapp.com/ws-blower")
    #ws = Websocket("http://192.168.0.13:8080/ws")
#asynd def connect():
    #global ws
    print("waiting")

    msg = await ws.get()
    robotDescription = await conn.getLocalDescription(msg)
    ws.put_nowait(robotDescription)
    print("Started WebRTC")
    await ws.close()
turnJet = False
def turnBlower():
    global turnJet
    while turnJet:
   # setServoPulse(2,2500)
      for i in range(700,2200,100):  
        pwm.setServoPulse(5,i)   
        time.sleep(0.02)     
        
      for i in range(2200,700,-100):
        pwm.setServoPulse(5,i) 
        time.sleep(0.02)

throttle = 600
def validator(num, upper=2500, lower=500):
    if num > upper:
        num = upper
    if num < lower:
        num = lower
    return num

def incrementer(cmd):
    global throttle
    global turnJet
    if cmd == 'up':
        throttle = validator(throttle + 100)
        pwm.setServoPulse(5, throttle)

    if cmd == 'down':
        throttle = validator(throttle - 100)
        pwm.setServoPulse(5, throttle)

    if cmd == 'left':
        turnJet = False
    if cmd == 'right':
        turnJet = True


    print(throttle)
    return throttle
        
async def cmnd():
    while True:
      msg = await conn.get()
      commands = msg.split(':')
      

      if commands[0] == 'button' and commands[1]== 'dpad':
          incrementer(commands[2])
      if commands[0] == 'button' and commands[1]== 'plow':
          if commands[2] == 'up':
              pwm.setServoPulse(5, 2000)
          if commands[2] == 'down':
              pwm.setServoPulse(5, 1000)
      if commands[0] == 'servo':
          pwm.setServoPulse(int(commands[1]), int(commands[2]))
          

              
          
      
      print("got", msg)
      
      if msg == "stop":
          pwm.setServoPulse(0, 1500)
          pwm.setServoPulse(1, 1500)
      elif msg == "left":
          pwm.setServoPulse(1, 1200)
      elif msg == "forward" or msg == "up":
          pwm.setServoPulse(0, 1300)
      elif msg == "back" or msg == "down":
          pwm.setServoPulse(0, 1700)
      elif msg == "right":
          pwm.setServoPulse(1, 1800)
      elif msg == "lightson":
          pwm.setServoPulse(4, 500)
          time.sleep(.1)
          pwm.setServoPulse(4, 2500)
    

         

        
      #await ws.close()
    

asyncio.ensure_future(connect())
asyncio.ensure_future(cmnd())
try:
    asyncio.get_event_loop().run_forever()
finally:
    cam.close()
    conn.close()


