# -*- coding: utf-8 -*-
import json
import twisted
from twisted.internet import reactor
import autobahn
#import os
#import yaml
#import pickle
from autobahn.websocket import WebSocketClientFactory
from autobahn.websocket import WebSocketClientProtocol
from autobahn.websocket import connectWS

host = "ws://localhost:9002" 
LOOP_TIME =  0.05

kinectClientInstance = None

class KinectControl():
    
    def __init__(self, host=host, save_data=None, loop_time=LOOP_TIME, reactor=reactor): 
        if save_data is None:
            save_data=self.save_data            
        factory = ClientFactory(host, save_data)
        factory.protocol = KinectClient
        connectWS(factory)
        self.reactor=reactor
        self.data = [{'RightHand':{"X":0, "Y":0}, 'RightShoulder':{"X":0, "Y":0}}]
        self.kk = None
        self.kin_parameter = None
 #       self.loaddata
       
#    def loaddata(self):

        
    def save_data(self, data):
        self.data = data
    
    def get_rel_pos(self):
        everything = self.data
        #print self.data
        if len(everything) > 0:
            try:
                x = (everything[0]['RightHand']['X']) - (everything[0]['RightShoulder']['X'])
                y = (everything[0]['RightHand']['Y']) - (everything[0]['RightShoulder']['Y'])
                pos = (x,y)
                return pos
            except Exception as e:
                print e
                
        else:
            return (0,0)
    
    def get_pos(self):
        everything = self.data
        if len(everything) > 0:
            try:
                position = (everything[0]['RightHand']['X'], everything[0]['RightHand']['Y'])
                return position
            except Exception as e:
                print e
                print self.data
                return (0, 0)

        else:
            return (0, 0)
            
    def set_cal_parameters(self, parameters):
        self.kin_parameter = parameters
        print parameters            
            
    def get_cal_pos(self):
        position = self.get_pos
        
        if self.kin_parameter == None:
            return position
        else:
            borders = self.kin_parameter
        
            leva = borders[1]
            prava = borders[2]
            up = borders[3]
            down = borders[0]
            
            delka = prava - leva
        
            if position[0] >= prava:
                new_pos = (1, position[1])
                print new_pos
                return new_pos
            elif position[0] <= leva:
                new_pos = (0, position[1])
                print new_pos
                return new_pos
            elif position[0] > leva and position[0] < prava:
                pos_delka = prava - position[0]
                new_pos = (float(pos_delka)/float(delka), position[1])
                print new_pos
                return new_pos
        
    def get_people(self):
        everything = self.data
        return len(everything)
        
    def print_pos(self):
        print self.data
       
class KinectClient(WebSocketClientProtocol):
    
    
    def sendSkeletonRequest(self):
        #print "Skeleton request"
        self.sendMessage("skeleton")
        
        
    def onMessage(self, msg, binary):
        if len(msg) > 2:
            #print msg
            data = json.loads(msg)
            self.factory.save_data_fcn(data)

        twisted.internet.reactor.callLater(LOOP_TIME, self.sendSkeletonRequest)
 
    def onOpen(self):
        #print 'On open'
        self.sendSkeletonRequest()

class ClientFactory(autobahn.websocket.WebSocketClientFactory):
    
    def __init__(self, host, save_data_fcn):
        autobahn.websocket.WebSocketClientFactory.__init__(self, url=host, debug=False)
        self.save_data_fcn = save_data_fcn

    def clientConnectionLost(self, connector, reason):
        print "connection lost"
    
    def clientConnectionFailed(self, connector, reason):
        print "connection failed"


def print_pos_repeated(kcontrol, loop_time = 1):
    pos = kcontrol.get_cal_pos()
    print pos
    reactor.callLater(loop_time, print_pos_repeated, kcontrol)

if __name__ == "__main__":
    kin = KinectControl()
    rr = reactor.callLater(1, print_pos_repeated, kin)
    reactor.run()