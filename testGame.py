<<<<<<< HEAD
import citygate
import random
import os
import sys
import msvcrt 
import math
import pygame
import time
import pickle

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

class TestGame(object):
        def __init__(self):
##                pygame.init()
                self.playerId = None
                self.running = 0
                self.parameters = self.get_parameters()
                self.game = GameLogic(self.parameters)
                self.graphics = GameGraphics(self.game,(1000, 600))
                self.game.setCorners (self.graphics.prava,self.graphics.leva,self.graphics.nahore,self.graphics.dole)
                self.fpsClock = pygame.time.Clock()
                self.m_pos = pygame.mouse.get_pos()
                self.click = 0
                self.actual_time = time.time()
                self.prev_time = 0
                self.pokynKHre = 0
                self.spusteno = 0
                self.defaut_parameters = {
                'ip_server':'192.168.1.5', 
                'host':True,
                'nplayers':2,
                'control1':'mouse',
                'window_size': (1024,768)
                }

        def get_parameters(self):
                config_file = 'pycanoid.config'
                if os.path.isfile(config_file):
                    stream = file(config_file, 'r')    # 'document.yaml' contains a single YAML document. # file() delal problemy na win 8 HOLI
                    if parse_version(sys.version) < parse_version('3.0'):
#               python 27
                        parameters = yaml.load(stream)
                    else: # python 3
                        parameters = yaml.load(stream)
                else:
                    parameters = self.defaut_parameters
                    if parse_version(sys.version) < parse_version('3.0'):
#               python 27
                        with open(config_file, 'wb') as f:
                            yaml.dump(parameters, f)
                    else: # python 3
                        with open(config_file, 'wb') as f:
                            yaml.dump(parameters, f)
                return parameters        
                
	def name(self):
		return "TestGame + Pycanoid"
	def author(self):
		return "Jakub Vit"
	def version(self):
		return "0.2 beta"
	def createGameState(self, mode):		
		state = citygate.State(mode)
		state.addParam('isPlayedS', 'float')
		state.addParam('ballXS', 'float')
		state.addParam('ballYS', 'float')
		state.addParam('paddle1PosS', 'float')
		state.addParam('paddle2PosS', 'float')
		state.addParam('paddle1PosYS', 'float')
		state.addParam('paddle2PosYS', 'float')
		state.addParam('startAngleS', 'float')		
		
		return state
	    
	def updateGameState(self, state, playerState, client, delta):
##                if playerState['isPlayedC'] == 1:
##                        state['isPlayedS'] = 1

                 

                # information about client paddles to server paddles
                if playerState['idPlayerC'] == 0:        
                        state['paddle1PosS'] = playerState['paddle1PosC']
                if playerState['idPlayerC'] == 1:          
                    state['paddle2PosS'] = playerState['paddle2PosC']


                state['paddle1PosYS'] = playerState['paddle1PosYC']
                state['paddle2PosYS'] = playerState['paddle2PosYC'] 
                self.game.paddle1.x = state['paddle1PosS'] -self.game.paddle1.size[0]/2
                self.game.paddle1.y = state['paddle1PosYS']
                self.game.paddle2.x = state['paddle2PosS'] -self.game.paddle1.size[0]/2
                self.game.paddle2.y = state['paddle2PosYS']

                #COMPUTING OF BALL - SERVER ONLY
                if client.isServer==True:

                    for i,p in client.players.iteritems():
                            if p['isPlayedC']==1:
                               print "jsem tu" 
                               state['isPlayedS'] = 1
                
                    if state['isPlayedS'] == 0:
                        self.spusteno = 0
                        self.game.setBallInGame(0)
                        self.game.GenerateAngle()
                        self.graphics.DrawBallBegin()
                        state['ballXS']=self.game.ball.x 
                        state['ballYS']=self.game.ball.y
                        
                        
                    if state['isPlayedS'] == 1:
                        self.game.setBallInGame(1)
                        if self.spusteno == 0:
                            self.prev_time = time.time() - 0.02
                            self.spusteno =1
                        elif  self.spusteno == 1:
                            self.prev_time = self.actual_time
                            
                        self.actual_time = time.time()
                        dt = self.actual_time - self.prev_time

                        
                        self.game.moveBall(dt)

                    
                        state['ballXS']=self.game.ball.x 
                        state['ballYS']=self.game.ball.y 

                        if self.game.isBallInGame() == 0:
                            state['isPlayedS'] = 0
                            for i,p in client.players.iteritems():
                                p['isPlayedC']=0
                                
##                        print state['clickTimeS']
                    os.system('cls')
                    print 'je ball ve hre [server]' + str(self.game.isBallInGame())
                    print self.spusteno
##                    print 'ball [server] x:' + str(self.game.ball.x) + ' y:' + + str(self.game.ball.y)
##                    print 'pad1: x:' + str(state['paddle1PosS'])+' y:'+str(state['paddle1PosYS'])
##                    print 'pad2: x:' + str(state['paddle2PosS'])+' y:'+str(state['paddle2PosYS'])

                    for i,p in client.players.iteritems():
                        print 'je ball hrace ve hre? [klient '+ str(i+1) +']: ' + str(p['isPlayedC'])
                        print 'pozice paddle 1 [klient '+ str(i+1) +']: ' + str(p['paddle1PosC'])
                        print 'pozice paddle 2 [klient '+ str(i+1) +']: ' + str(p['paddle2PosC'])

                
                
	def createPlayerState(self, mode):
		state = citygate.State(mode)
		state.addParam('isPlayedC', 'float', False)
		state.addParam('idPlayerC', 'float', False)
		state.addParam('paddle1PosC', 'float', False)
                state.addParam('paddle2PosC', 'float', False)
                state.addParam('paddle1PosYC', 'float', False)
                state.addParam('paddle2PosYC', 'float', False)
		return state
	def updatePlayerState(self, state, playerId, gameState, delta):
                
                if not playerId == None:
                    state['idPlayerC'] = playerId
                    state['paddle1PosYC']= self.game.paddle1.y
                    state['paddle2PosYC']= self.game.paddle2.y
##                print playerId      
	
		#print state['pos']
	def createGUI(self):
                pygame.init()
                # Control
                if self.parameters['control1'] == 'face':
                    fctrl = facecontrol.Facecontrol()
                # Nastaveni FPS
                FPS = 60
                self.fpsClock = pygame.time.Clock()
                pygame.display.update()

                self.running = 1
##                self.click = 0

	def render(self, client):
                if self.running==1:  
                        self.graphics.CreateBackground()
                        if self.parameters['control1'] == 'mouse':
                            m_pos = pygame.mouse.get_pos()                  
                       
                        if self.playerId == 0:
                            self.graphics.DrawDesk(m_pos, self.game.paddle1, 0)
                            self.graphics.DrawDesk([client.gameState['paddle2PosS'],0], self.game.paddle2, 1)
                        if self.parameters['nplayers'] == 2:
                            if self.playerId == 1: 
                                self.graphics.DrawDesk([client.gameState['paddle1PosS'],0], self.game.paddle1, 0)
                                self.graphics.DrawDesk(m_pos, self.game.paddle2, 1)

                        self.graphics.DrawInformations(self.game)    
                        if client.gameState['isPlayedS'] == 0:
                            self.graphics.DrawBallBegin()
                             
                        elif client.gameState['isPlayedS'] == 1:                    
                            self.graphics.obrazovka.blit(self.graphics.ball_surface, (client.gameState['ballXS']- 0, client.gameState['ballYS']))#PREPSAT TU PADESATKU
                            
                    


                        
   
                        pygame.display.update()
                        FPS = 60
                        self.fpsClock.tick(FPS)
                        
		os.system('cls')
		print "Test Game"
                print
		print 'je ball ve hre? [server]: ' + str(client.gameState['isPlayedS'])
		print 'ball [server] x: ' + str(client.gameState['ballXS']) + ' y: ' + str(client.gameState['ballYS'])
                print 'paddle 1 [server] :' + str(client.gameState['paddle1PosS'])
                print 'paddle 2 [server] :' + str(client.gameState['paddle2PosS'])
                print
                print self.game.ball.x
                print self.game.ball.y
                print

		for i,p in client.players.iteritems():
                        print 'je ball hrace ve hre? [klient '+ str(i+1) +']: ' + str(p['isPlayedC'])
                        print 'pozice paddle 1 [klient '+ str(i+1) +']: ' + str(p['paddle1PosC'])
                        print 'pozice paddle 2 [klient '+ str(i+1) +']: ' + str(p['paddle2PosC'])
			
	def handleUserInput(self, playerState, gameState, client):
                
                mouse = pygame.mouse.get_pos()



                        
##                if playerState['isPlayedC'] == 1:
##                    self.game.setBallInGame(1)

                            
                playerState['isPlayedC'] = self.game.isBallInGame()
                
                if playerState['idPlayerC']==0:
                        self.playerId = 0
                        playerState['paddle1PosC']=mouse[0]
                if playerState['idPlayerC']==1:
                        self.playerId = 1
                        playerState['paddle2PosC']=mouse[0]
                
                for event in pygame.event.get():
                            if event.type == pygame.QUIT:                                    
                                self.running = 0
                                pygame.display.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN and playerState['idPlayerC']==0:
                                self.start = 1
                                self.prev_time = time.time()
                                self.actual_time = time.time()
##                                self.game.setBallInGame(1)

                                playerState['isPlayedC'] = 1
##                                gameState['isPlayedS'] = 1
                                
                                
                                
		

if __name__ == "__main__":
	myGame = citygate.runGame(TestGame())
=======
import citygate

import random
import os
import sys
import msvcrt 
import math

class TestGame(object):
	def name(self):
		return "TestGame"
	def author(self):
		return "Jakub Vit"
	def version(self):
		return "0.1 beta"
	def createGameState(self, mode):		
		state = citygate.State(mode)
		state.addParam('pos', 'float')
		state.addParam('dir', 'float', defaultValue = 1)
		return state
	def updateGameState(self, state, delta):
		state['pos'] += state['dir'] * delta * 10		
		if state['pos'] > 50:
			state['pos'] = 50
			state['dir'] = -1
		if state['pos'] < 0:
			state['pos'] = 0
			state['dir'] = +1
	def createPlayerState(self, mode):
		state = citygate.State(mode)	
		state.addParam('pos', 'float', False)
		state.addParam('dir', 'float', False)
		return state
	def updatePlayerState(self, state, delta):
		state['pos'] = max(0, min(50, state['pos'] + state['dir'] * 5 * delta))		
		#print state['pos']
	def createGUI(self):
		#os.system('cls')
		pass
	def render(self, client):	
		os.system('cls')
		print "Test Game"
		print "Num1: left, Num2: stop, Num3: right"
		print
		
		ballPos = int(client.gameState['pos'])			
		print ' server: ' + '.' * (ballPos - 1) + 'x' + '.' * (50 - ballPos - 2)	
			
		for i,p in client.players.iteritems():
			pos = int(p['pos'])
			print 'player' + str(i) + ': ' + '.' * (pos - 1) + 'x' + '.' * (50 - pos - 2)		
	def handleUserInput(self, playerState):
		keyPressed = msvcrt.kbhit()
		if keyPressed:
			c = msvcrt.getch()
			if c == '3':
				playerState['dir'] = 1
			elif c == '1':
				playerState['dir'] = -1
			elif c == '2':
				playerState['dir'] = 0

if __name__ == "__main__":
	citygate.runGame(TestGame())
>>>>>>> d0cfc7e7dc765c1e70ab41859b179ee7babf0aa2
