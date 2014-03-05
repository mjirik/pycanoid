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


host = "ws://148.228.186.59:9002" 
host = "ws://localhost:9002" 

data = None

class KinectControl():
#   def 
#    def get_pos()

class KinectClient(WebSocketClientProtocol):
    
    def sendSkeletonRequest(self):
        self.sendMessage("skeleton")
        
    def onMessage(self, msg, binary):
        
        if len(msg) > 0:
            self.data = json.loads(msg)
            print self.data[0]['Head']
            data = self.data

    def onOpen(self):
        self.sendSkeletonRequest()
        
        
if __name__ == "__main__":
    #pygame.init()
    factory = WebSocketClientFactory(host, debug = False)
    factory.protocol = KinectClient
    print "sdfas"
    connectWS(factory)
    print "sdfas"
    reactor.run()