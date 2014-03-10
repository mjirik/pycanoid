# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:57:37 2014

@author: tstation
"""
import json
import twisted
from twisted.internet import reactor
import os, sys, pygame
import autobahn
from autobahn.websocket import WebSocketClientFactory
from autobahn.websocket import WebSocketClientProtocol
from autobahn.websocket import connectWS


#host = "ws://148.228.186.59:9002" 
host = "ws://localhost:9002" 
LOOP_TIME =  6


kinectClientInstance = None

class KinectControl():
    
    def __init__(self): # , reactor=reactor): 
        self.data = []
        self.kk = None
       
      
    def set_KinectKlient(self,kk):
        self.kk = kk
        pass

    def set_reactor(self, reactor):
        self.reactor=reactor
   
    def save_data(self, data):
        print "save data"
        self.data = data
    
    def get_pos(self):
        print "Position"
        position = self.data
        return position
       
class KinectClient(WebSocketClientProtocol):
    
    
    #def onOpen(self):
    #    print "open"
    #    self.send_skel_request_loop()
    
    def sendSkeletonRequest(self):
        print "Skeleton request"
        self.sendMessage("skeleton")
        
    #def send_skel_request_loop(self):
    #    print "Skeleton request"
    #    self.sendMessage("skeleton")
    #    twisted.internet.reactor.callLater(LOOP_TIME, self.send_skel_request_loop)
        
        
        
    def onMessage(self, msg, binary):
        print "On message"
        print msg
        
        if len(msg) > 2:
            data = json.loads(msg)
#            complete_data = self.data
#            print 'Data: ',self.data
#            print dir(self.factory)
#            print "pred save data"
#            print self.data
            self.factory.save_data_fcn(data)
#            print "pred call later"
#
#            print "po call later"
#            #self.sendSkeletonRequest()
#        else:
#            print "No msg"

        #self.factory.app.reactor.callLater(LOOP_TIME, self.sendSkeletonRequest)
        twisted.internet.reactor.callLater(LOOP_TIME, self.sendSkeletonRequest)
        #twisted.internet.reactor.callLater(LOOP_TIME, fcn, "dsadsaf")
        #twisted.internet.reactor.callLater(LOOP_TIME, self.sendMessage, "skeleton")
    
    #def process(self, data):
    #    return data        
        
    def onOpen(self):
        print 'On open'
        self.sendSkeletonRequest()
        #self.send_skel_request_loop()
        
#class 

class ClientFactory(autobahn.websocket.WebSocketClientFactory):
    
    #self.protocol = WebSocketClientProtocol
    
    def __init__(self, host, save_data_fcn):
        autobahn.websocket.WebSocketClientFactory.__init__(self, url=host, debug=False)
        self.save_data_fcn = save_data_fcn
        #self.app = app

#####################################################
#####################################################
        
    def clientConnectionLost(self, connector, reason):
        #self.app.main_window.set_online_status(False)
        #self.app.main_window.btn_connect.setEnabled(True)
        print "connection lost"
    
    def clientConnectionFailed(self, connector, reason):
        #self.app.main_window.set_online_status(False)
        #self.app.main_window.btn_connect.setEnabled(True)
        print "connection failed"


def fcn(a):
    print a
    #reactor.callLater(2, fcn, "ahojjj print")

if __name__ == "__main__":

    kin = KinectControl()  #reactor)
    #kin.set_reactor(reactor)

    factory = ClientFactory(host, kin.save_data)
    factory.protocol = KinectClient
    connectWS(factory)
    reactor.callLater(5, fcn, "ahojjj print")
    reactor.run()

    #print "pred get pos"
    #neco = kin.get_pos()
    
    
    
    #print neco
    
    #react = reactor
    #react.run()
    
    
        
    
   # factory = WebSocketClientFactory(host, debug = False)
   # factory.protocol = KinectClient
   # connectWS(factory)
   # reactor.run()