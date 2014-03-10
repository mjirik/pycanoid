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

complete_data = []

kinectClientInstance = None

class KinectControl():
    
   def __init__(self):
       self.data = []
       self.kk = None
       
      
   def set_KinectKlient(self,kk):
       self.kk = kk
       pass
   
   def save_data(self, data):
       print "save data"
       self.data = data
    
   def get_pos(self):
       print "Position"
       position = self.data
       return position
       
class KinectClient(WebSocketClientProtocol):
    
    def sendSkeletonRequest(self):
        print "Skeleton request"
        self.sendMessage("skeleton")
        
    def onMessage(self, msg, binary):
        print "On message"
        if len(msg) > 2:
            self.data = json.loads(msg)
            complete_data = self.data
            print 'Data: ',self.data
            print dir(self.factory.app)
            print "pred save data"
            self.factory.app.save_data(self.data)
            #self.sendSkeletonRequest()
        else:
            print "No msg"
    
    def process(self, data):
        return data        
        
    def onOpen(self):
        print 'On open'
        self.sendSkeletonRequest()
        
#class 

class ClientFactory(autobahn.websocket.WebSocketClientFactory):
    
    #self.protocol = WebSocketClientProtocol
    
    def __init__(self, host, app):
        autobahn.websocket.WebSocketClientFactory.__init__(self, url=host, debug=False)
        self.app = app

#####################################################
#####################################################
        
    def clientConnectionLost(self, connector, reason):
        self.app.main_window.set_online_status(False)
        self.app.main_window.btn_connect.setEnabled(True)
        print "connection lost"
    
    def clientConnectionFailed(self, connector, reason):
        self.app.main_window.set_online_status(False)
        self.app.main_window.btn_connect.setEnabled(True)
        print "connection failed"

        
if __name__ == "__main__":



    kin = KinectControl()

    factory = ClientFactory(host, kin)
    factory.protocol = KinectClient
    connectWS(factory)
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