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