#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time
import math
import random
import pickle
import os
import sys

from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from pycanoidGameLogic import GameLogic
from pycanoidGraphics import GameGraphics

from gamearea import Gamearea
import facecontrol
import kinectcontrol

# version comparison
from pkg_resources import parse_version

if parse_version(sys.version) < parse_version('3.0'):
       # python 2.7
       import yaml
else:
      # python 3.0
       import yaml
       pass


class Pycanoid:
    def __init__(self):
        self.defaut_parameters = {
            'ip_server': '192.168.1.5',
            'host': True,
            'nplayers': 2,
            'control1': 'face',
            'window_size': (1024, 768)
        }

    def get_parameters(self):
        """
        Funkce obstará základní parametry
        """
        config_file = 'pycanoid.config'
        if os.path.isfile(config_file):
            stream = file(config_file,
                          'r')    # 'document.yaml' contains a single YAML document. # file() delal problemy na win 8 HOLI
            if parse_version(sys.version) < parse_version('3.0'):
            #           python 27
                parameters = yaml.load(stream)
            else: # python 3
                parameters = yaml.load(stream)
        else:
            parameters = self.defaut_parameters
            if parse_version(sys.version) < parse_version('3.0'):
            #           python 27
                with open(config_file, 'wb') as f:
                    yaml.dump(parameters, f)
            else: # python 3
                with open(config_file, 'wb') as f:
                    yaml.dump(parameters, f)
        return parameters


    def game_tick(self):
        self.click = self.game.isBallInGame()
        self.graphics.CreateBackground()
        # Control
        if self.parameters['control1'] == 'mouse':
            m_pos = pygame.mouse.get_pos()    # aktuální pozice myši
        elif self.parameters['control1'] == 'face':  # Face control
            # Loading game area parameters
            if os.path.exists("area_params.ps"):
                f = open("area_params.ps", 'rb')
                area = pickle.load(f)
                f.close()

                # Setting parameters
                self.ctrl.set_calibration_params(area)
                # Calibrated position
                m_pos = ((self.ctrl.get_pos()[0] * self.defaut_parameters['window_size'][0]),
                         (self.ctrl.get_pos()[1] * self.defaut_parameters['window_size'][1]))
            else:
                print "Run camera calibration first"
                raise Exception('Run camera calibration first', 'Run camera calibration first')
        elif self.parameters['control1'] == 'kinect':  # Face control
            m_pos = self.ctrl.get_pos()

        # Graphics
        self.graphics.DrawDesk(m_pos, self.game.paddle1, 0)
        if self.parameters['nplayers'] == 2:
            self.graphics.DrawDesk(m_pos, self.game.paddle2, 1)

        # Začátek hry
        self.graphics.DrawBlocks()
        if self.game.isBallInGame() == 0:
            self.game.GenerateAngle()
            self.graphics.DrawBallBegin()

        # Akce start
        elif self.game.isBallInGame() == 1:
            prev_time = self.actual_time
            self.actual_time = time.time()
            dt = self.actual_time - prev_time
            self.game.moveBall(dt)
            self.click = self.game.isBallInGame()
            self.graphics.obrazovka.blit(self.graphics.ball_surface, (self.game.ball.x, self.game.ball.y))
            self.graphics.DrawInformations(self.game)


        ##        # Kontrola provedených akcí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # Ukončení aplikace stisknutím křížku
                self.running = 0
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Aktivace tlačítka na myši
                prev_time = time.time()
                self.actual_time = time.time()
                self.game.setBallInGame(1)
            ##
            ##
            ##        # synchronizace po síti
            ##        if parameters['nplayers'] > 1:
            ##            game_state = mux_game_state(deska, deska2, ball)
            ##            game_state = comunication_loop(game_state, comunication_parameters)
            ##            deska, deska2, ball = demux_game_state(game_state, deska, deska2, ball)
            ##
            ##
        pygame.display.update()

    def run(self):

        pygame.init()

        self.parameters = self.get_parameters()

        self.game = GameLogic(self.parameters)
        self.graphics = GameGraphics(self.game, (1000, 600))
        self.game.setCorners(self.graphics.prava, self.graphics.leva, self.graphics.nahore, self.graphics.dole)

        # Control
        if self.parameters['control1'] == 'face':
            self.ctrl = facecontrol.Facecontrol()
        if self.parameters["control1"] == "kinect":
            self.ctrl = kinectcontrol.KinectControl()
            host = "ws://localhost:9002" 
           # factory = kinectcontrol.ClientFactory(host, ctrl)
            #factory.protocol = kinectcontrol.KinectClient
            #kinectcontrol.connectWS(factory)
        else:
            self.ctrl = None
        # Nastaveni FPS
        FPS = 60
        fpsClock = pygame.time.Clock()

        pygame.display.update()

        self.running = 1
        self.click = 0

        print (self.graphics.spodni_levy[1] - self.graphics.horni_levy[1] - 1)
        
        # Set up a looping call every 1/30th of a second to run your game tick
        tick = LoopingCall(self.game_tick)
        tick.start(1.0 / FPS)

# Set up anything else twisted here, like listening sockets
        
        reactor.run() # Omit this if this is a tap/tac file
        #reactor.run()
        #while self.running:
        #    self.game_tick(game, graphics, parameters, ctrl)
        #    fpsClock.tick(FPS)


if __name__ == "__main__":
    pycanoid = Pycanoid()
    pycanoid.run()
