#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import time
import math
import random
#import pickle
import os
import sys

from pycanoidGameLogic import GameLogic
from pycanoidGraphics import GameGraphics

from gamearea import Gamearea
import facecontrol

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
                'ip_server':'192.168.1.5', 
                'host':True,
                'nplayers':2,
                'control1':'face',
                'window_size': (1024,768)
                }

    def get_parameters(self):
        """
        Funkce obstará základní parametry
        """
        config_file = 'pycanoid.config'
        if os.path.isfile(config_file):
            stream = file(config_file, 'r')    # 'document.yaml' contains a single YAML document. # file() delal problemy na win 8 HOLI
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

    def run(self):

        pygame.init()

        parameters = self.get_parameters()

        game = GameLogic(parameters)    
        graphics = GameGraphics(game,(1000, 600))
        game.setCorners (graphics.prava,graphics.leva,graphics.nahore,graphics.dole)

        # Control
        if parameters['control1'] == 'face':
            fctrl = facecontrol.Facecontrol()
# Nastaveni FPS
        FPS = 60
        fpsClock = pygame.time.Clock()

        pygame.display.update()

        running = 1
        click = 0

        print (graphics.spodni_levy[1]-graphics.horni_levy[1]-1)
        while running:  
                click = game.isBallInGame()
                graphics.CreateBackground()
# Control
                if parameters['control1'] == 'mouse':
                    m_pos = pygame.mouse.get_pos()    # aktuální pozice myši
                elif parameters['control1'] == 'face':
                    m_pos = fctrl.get_pos()
# Graphics
                graphics.DrawDesk(m_pos, game.paddle1, 0)
                if parameters['nplayers'] == 2:
                        graphics.DrawDesk(m_pos, game.paddle2, 1)

                # Začátek hry       
                if game.isBallInGame() == 0:
                    game.GenerateAngle()
                    graphics.DrawBallBegin()
                    
                # Akce start
                elif game.isBallInGame() == 1:
                    prev_time = actual_time
                    actual_time = time.time()
                    dt = actual_time - prev_time
                    game.moveBall(dt)
                    click = game.isBallInGame()
                    graphics.obrazovka.blit(graphics.ball_surface, (game.ball.x, game.ball.y))
                    graphics.DrawInformations(game)
                    

##        # Kontrola provedených akcí
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:               # Ukončení aplikace stisknutím křížku
                        running = 0
                        pygame.display.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:  # Aktivace tlačítka na myši              
                        prev_time = time.time()
                        actual_time = time.time()
                        game.setBallInGame(1)
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
                fpsClock.tick(FPS)

if __name__ == "__main__":
    pycanoid = Pycanoid()
    pycanoid.run()
