import kinectcontrol
import time
import yaml
#import pickle
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class kinec_calib():
     
    def __init__(self):
        self.ctrl = kinectcontrol.KinectControl()
        self.FPS = 30
        self.polex = []
        self.poley = []
        self.start = time.time()
         
    def ready(self):
        #self.pole = []
        print 'Get to position'
        start = time.time()
        done = False
        
        while not done:
            now = time.time()
            if (now - start) >= 5:
                done = True
        
        print "Tracking"
        self.start = time.time()
        self.run()
        
    
    def run(self):
        #self.tick = 
        reactor.callLater(1.0 / self.FPS , self.game_tick)
        #print self.tick
        #self.tick.start(1.0 / self.FPS)        
        #reactor.run()
        
            
    def game_tick(self):
        position = self.ctrl.get_pos()
        print position
        if position != (0,0):
            self.polex.append(position[0])
            self.poley.append(position[1])
            now = time.time()
            if now - self.start >= 10:                
                print "stop reactor"
                reactor.stop()
                self.save_data()
                
        reactor.callLater(1.0 / self.FPS , self.game_tick)

    def save_data(self):
        polex = self.polex
        poley = self.poley
        
        left = min(polex)
        right = max(polex)
        top = max(poley)
        bottom = min(poley)
        borders = {'left': left, 'right': right, 'top': top, 'bottom': bottom}        
        print borders
        print "Saving"
        fil = file('kinect_borders.config','wb')
        yaml.dump(borders, fil)
        #fil.close()
    
if __name__ == '__main__':
    k = kinec_calib()
    print "Get to position"
    
    reactor.callLater(5, k.game_tick)
    k.start = time.time()    
    reactor.run()
    
    #borders = k.get_borders()
    #print borders
         