import RPi.GPIO as g
import time
g.setmode(g.BCM)
on = g.HIGH
off = g.LOW
class Tank:
    def __init__(self, p1,p2,p3,p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        g.setup(p1, g.OUT)
        g.setup(p2, g.OUT)
        g.setup(p3, g.OUT)
        g.setup(p4, g.OUT)
    def test(self, chan):
        g.output(chan, on)
        time.sleep(1)
        g.output(chan, off)
    def stop(self):
        g.output(self.p1, off)
        g.output(self.p2, off)
        g.output(self.p3, off)
        g.output(self.p4, off)
        
    def forward(self):
        g.output(self.p1, on)
        g.output(self.p3, on)
    
    def back(self):
        g.output(self.p2, on)
        g.output(self.p4, on)
    
    def left(self):
        g.output(self.p1, on)
        g.output(self.p4, on)
    
    def right(self):
        g.output(self.p2, on)
        g.output(self.p3, on)





    


