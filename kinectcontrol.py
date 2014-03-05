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

data = {"LeftHand":{"X":0, "Y":0}}

kinectClientInstance = None

class KinectControl():
    
   def __init__(self):
      self.factory = WebSocketClientFactory(host, debug = False)
      self.factory.protocol = KinectClient
      connectWS(self.factory)
      print "KC init"
      print kinectClientInstance
      print dir(kinectClientInstance)
      
    
    #reactor.run()

    
   def get_pos(self):
       
       positionX = data["LeftHand"]['X']
       positionY = data["LeftHand"]['Y']
       position = (positionX, positionY)
       
       #self.factory.protocol.sendSkeletonRequest()
       return position

class KinectClient(WebSocketClientProtocol):
    
    def sendSkeletonRequest(self):
        print "send skeleton request"
        self.sendMessage("skeleton")
        
    def onMessage(self, msg, binary):
        print "on message"
        if len(msg) > 2:
            self.data = json.loads(msg)
            data = self.data[0]
            print data

    def onOpen(self):
        self.sendSkeletonRequest()
        #self.data = None
        print "on open"
        #kinectClientInstance = self
        print "on open"
        
if __name__ == "__main__":
    #kinect = KinectControl()
    factory = WebSocketClientFactory(host, debug = False)
    factory.protocol = KinectClient
    connectWS(factory)
    print "run"
    reactor.run()
    
    #print kinect.get_pos()
    
   #while True:
    #    print kinect.get_pos()
#    #pygame.init()
 #   factory = WebSocketClientFactory(host, debug = False)
  #  factory.protocol = KinectClient
   # print "sdfas"
    #connectWS(factory)
   # print "sdfas"
   # reactor.run()