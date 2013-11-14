import enet
import sys
import getopt
import time
from pprint import pprint
import string
import random
import pickle


class StateMode:
	SERVER = 1
	CLIENT_LOCAL = 2
	CLIENT_REMOTE = 3

class State(object):
	def __init__(self, mode):
		self.mode = mode
		self.values = {}
		
	def addParam(self, name, type = 'float', ownedByServer = True, defaultValue = 0):
		owner = False	
		if (ownedByServer and self.mode == StateMode.SERVER) or (not ownedByServer and self.mode == StateMode.CLIENT_LOCAL):
			owner = True
		self.values[name] = {
			'value': defaultValue,
			'type': type,
			'owner': owner
		}

	def updateFromPacket(self, str):
		d = pickle.loads(str)
		for i in self.values:
			if self.values[i]['owner'] == True:
				continue			
			val = self.values[i]['value']
			t = self.values[i]['type']
			if t == 'float':
				val = float(val)
			if not i in d:
				print "Key does not exist"
				print d
			self.values[i]['value'] = d[i]['value']		
		
	def formatPacket(self):
		data = {}
		for i in self.values:
			data[i] = {
				'value': self.values[i]['value']
			}	
		packetData = pickle.dumps(data)		
		return packetData

	def __str__(self):
		s = ""
		for i in self.values:
			s += str(i) + ":" + str(self.values[i]['value']) + ";"
		return s
 
	def __getitem__(self, index):
		return self.values[index]['value']

	def __setitem__(self, key, value):
		if not key in self.values:
			print "Key does not exist"
			print self.values
		self.values[key]['value'] = value
	
class Game(object):
	def name(self):
		raise NotImplementedError()
	def author(self):
		raise NotImplementedError()
	def version(self):
		raise NotImplementedError()
	def createGameState(self, state):
		raise NotImplementedError()
	def updateGameState(self, state):
		raise NotImplementedError()
	def createPlayerState(self, state):	
		raise NotImplementedError()
	def updatePlayerState(self, state, delta):
		raise NotImplementedError()
	def handleUserInput(self, playerState):
		raise NotImplementedError()
	def createGUI(self):
		raise NotImplementedError()
	def render(self):
		raise NotImplementedError()
	

class ClientServer(object):
	def __init__(self, game, isServer):
		self.players = {}
		self.game = game
		self.localTime = -1
		self.timeDelta = 0
		self.isServer = isServer
		self.clientId = None
		self.clientConnected = False	
		self.gameState = None

	def onClientConnect(self, peer):
		pass
	def onClientDisconnect(self, peer):
		pass
	def onMessageRecieved(self, msg):
		pass
	def sendData(self):		
		pass
	def updatePlayers(self, delta):
		for i, s in self.players.iteritems():
			self.game.updatePlayerState(s, delta)
		#if self.isServer:
		self.game.updateGameState(self.gameState, delta)

	def debugPrint(self):
		print('................')
		for i, s in self.players.iteritems():
			if i == self.clientId:
				print('>'),
			else:
				print(' '),
			print(i, str(s))
		print('.',str(self.gameState))


	def run(self):
		if self.isServer:
			self.gameState = self.game.createGameState(StateMode.SERVER)
		else:
			self.gameState = self.game.createGameState(StateMode.CLIENT_REMOTE)
		start = time.clock()
		self.localTime = 0
		lastLocalTime = 0
		debugCounter = 0
		if not self.isServer:
			self.game.createGUI()
		while True:
			lastLocalTime = self.localTime			
			self.localTime = time.clock() - start	
			self.delta = self.localTime - lastLocalTime		
			self.updatePlayers(self.delta)			
			while True:
				event = self.host.service(0)
				if event == None:
					break
				elif event.type == enet.EVENT_TYPE_CONNECT:
					self.onClientConnect(event.peer)
				elif event.type == enet.EVENT_TYPE_DISCONNECT:
					self.onClientDisconnect(event.peer)
				elif event.type == enet.EVENT_TYPE_RECEIVE:
					msg = pickle.loads(event.packet.data)
					self.onMessageRecieved(msg)
			if not self.isServer and self.clientId != None:
				self.game.handleUserInput(self.players[self.clientId])
			self.sendData()
			debugCounter += self.delta
			if self.isServer and debugCounter > 2:
				#self.debugPrint()
				debugCounter = 0
			self.host.flush()
			if not self.isServer and self.clientId != None:
				self.game.render(self)
			time.sleep(0.1)

class GameServer(ClientServer):
	def __init__(self, game):
		super(GameServer,self).__init__(game, True)

	def create(self, args):
		port = 6792
		try:
			opts, args = getopt.getopt(args, "p:", [])
		except getopt.error, msg:
			print msg
			sys.exit(2)
		for o, a in opts:
			if o in ("-p", "--port"):
				port = a
		self.host = enet.Host(enet.Address("*", port), 16, 0, 0, 0)
		print "Game server started ..."		

	def onClientConnect(self, peer):
		clientId = int(peer.incomingPeerID)
		print "New client connected", clientId
		self.players[clientId] = self.game.createPlayerState(StateMode.SERVER)


	def onClientDisconnect(self, peer):
		clientId = int(peer.incomingPeerID)
		print "players disconnected", clientId
		del self.players[clientId]

	def onMessageRecieved(self, msg):
		if msg['action'] == 'player_update':
			clientId = int(msg['clientId'])						
			self.players[clientId].updateFromPacket(msg['state'])
		if msg['action'] == 'game_update':
			self.gameState.updateFromPacket(msg['state'])

	def sendData(self):
		for i, s in self.players.iteritems():
			msg = pickle.dumps({
					'action': 'player_update',
					'clientId': str(i),
					'state': s.formatPacket()
				});
			packet = enet.Packet(msg)
			self.host.broadcast(0, packet)
		
		msg = pickle.dumps({
				'action': 'game_update',
				'time': self.localTime,
				'state': self.gameState.formatPacket()
		});
		packet = enet.Packet(msg)
		self.host.broadcast(0, packet)
	

	def stop(self):
		print "Stopping server ..."


class GameClient(ClientServer):
	def __init__(self, game):
		super(GameClient,self).__init__(game, False)

	def create(self, args):
		port = 6792
		ipAddress = "127.0.0.1"
		try:
			opts, args = getopt.getopt(args, "a:p:", [])
		except getopt.error, msg:
			print msg
			sys.exit(2)
		for o, a in opts:
			if o in ("-p", "--port"):
				port = int(a)
			if o in ("-a", "--address"):
				ipAddress = a
		self.host = enet.Host(None, 1, 0, 0, 0)
		self.peer = self.host.connect(enet.Address(ipAddress, port), 1)
		print "Game client connecting to " + ipAddress + ":" + str(port)	

	def onClientConnect(self, peer):
		self.clientConnected = True
		self.clientId = peer.outgoingPeerID	
		self.players[self.clientId] = self.game.createPlayerState(StateMode.CLIENT_LOCAL)
		print "Client connected with id=" + str(self.clientId)

	def onClientDisconnect(self, peer):
		pass

	def sendData(self):
		if self.clientId != None:
			s = self.players[self.clientId]
			msg = pickle.dumps({
					'action': 'player_update',
					'clientId': str(self.clientId),
					'state': s.formatPacket()
				});
			packet = enet.Packet(msg)
			self.peer.send(0, packet)

	def onMessageRecieved(self, msg):
		#print msg
		if msg['action'] == 'player_update':
			clientId = int(msg['clientId'])						
			if not clientId in self.players:
				self.players[clientId] = self.game.createPlayerState(StateMode.CLIENT_REMOTE)				
			self.players[clientId].updateFromPacket(msg['state'])	
		if msg['action'] == 'game_update':
			self.gameState.updateFromPacket(msg['state'])
			
	def stop(self):		
		if self.clientId != None:
			print "Discconnecting client ..."
        	self.peer.disconnect()
        	self.host.service(0)
        	self.host.flush()


def runGame(game):
	if len(sys.argv) < 2:
		print >> sys.stderr, "Missing mode parameter"
		sys.exit(1)
				
	if sys.argv[1] != "client" and sys.argv[1] != "server":
		print "Unknown mode option (either 'server' or 'client')"
		sys.exit(1)
			
	if sys.argv[1] == "server":
		isServer = True
	else:
		isServer = False
			
	print ""
	print "-------------------------------------------"
	print " " + game.name() + " (" + game.version() + ") by " + game.author()
	print "-------------------------------------------"
	print ""
	
	if isServer:
		gameObj = GameServer(game)
	else:
		gameObj = GameClient(game)
		
	gameObj.create(sys.argv[2:])
	try:
		gameObj.run()
	except KeyboardInterrupt:
		gameObj.stop()
	
	