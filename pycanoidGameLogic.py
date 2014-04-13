#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import time
import math
import random
import yaml
import os
import numpy as np

pygame.init()

class GameLogic:
    def __init__(self,parameters):
        #self.generateBlocks()
        self.parameters = parameters
        self.lives = 3
        self.takes = 0
        self.points = 0
        self.part = 3
        self.ballInGame = 0 # 1-ball is in game, 0- somebody has lost the ball or begining 
        self.paddle1 = Paddle()
        if parameters['nplayers'] == 2:
            self.paddle2 = Paddle()
        self.ball = Ball()
        self.kolize_blok = -1
        self.gone = False
        self.player = Player()

    def setkolize(self, blok):
        self.kolize_blok = blok

    def set_allgone(self, gone):
        self.gone = gone

    def generateBlocks(self):
        """
        Generuje pokazde nahodne bloky pro hru
        """
        matrix = np.random.randint(2, size=(10, 10))
        np.save('blockmap', matrix)
        self.player.GenerateName()

    def setCorners(self, prava, leva, nahore, dole):
        self.prava = prava  # X souřadnice pro pravou herní plochu
        self.leva = leva    # X souřadnice pro levou herní plochu
        self.nahore = nahore  # Y souřadnice pro horní stranu
        self.dole = dole   # Y souřadnice spodního kraje

    def moveBall(self, dt):
        dx = math.cos(self.ball.uhel) * self.ball.speed * dt   # Výpočet příštích souřadnic x,y
        dy = math.sin(self.ball.uhel) * self.ball.speed * dt

        self.ball.xp = self.ball.x                        # Posunutí aktuálních souřadnic do předchozích
        self.ball.yp = self.ball.y

        self.ball.x += dx                   # Výpočet nových souřadnic s kompenzací času
        self.ball.y += dy

        'Merici body na micku'
        mic_stred_prava = (self.ball.x+self.ball.size[0], self.ball.y+(self.ball.size[1]/2))
        mic_stred_leva = (self.ball.x, self.ball.y+(self.ball.size[1]/2))
        mic_stred_horni = (self.ball.x+(self.ball.size[0]/2), self.ball.y)
        mic_stred_spodni = (self.ball.x+(self.ball.size[0]/2), self.ball.y+self.ball.size[1])

        if self.kolize_blok != -1:  # doslo ke kolizi
            'Merici body na bloku'
            deska_stred_leva = (self.kolize_blok[0], self.kolize_blok[1]+(self.kolize_blok[3]/2))
            deska_stred_prava = (self.kolize_blok[0]+self.kolize_blok[2], self.kolize_blok[1]+(self.kolize_blok[3]/2))
            deska_stred_spodni = (self.kolize_blok[0]+(self.kolize_blok[2]/2), self.kolize_blok[1]+self.kolize_blok[3])
            deska_stred_horni = (self.kolize_blok[0]+(self.kolize_blok[2]/2),self.kolize_blok[1])

            'Test narazu do bloku'
            if (mic_stred_prava[0] >= deska_stred_leva[0]) and (mic_stred_leva[0] < deska_stred_leva[0]):
                self.reflectXright(self.kolize_blok[0])
            elif (mic_stred_leva[0] >= deska_stred_prava[0]) and (mic_stred_prava[0] > deska_stred_prava[0]):
                self.reflectXleft(self.kolize_blok[0]+self.kolize_blok[2])
            elif (mic_stred_horni[1] <= deska_stred_spodni[1]) and (mic_stred_spodni[1] > deska_stred_spodni[1]):
                self.reflectYup(self.kolize_blok[1]+self.kolize_blok[3])
            elif (mic_stred_spodni[1] >= deska_stred_horni[1]) and (mic_stred_horni[1] < deska_stred_horni[1]):
                self.reflectYdown(self.kolize_blok[1])

        paddle2_stred_dole = (self.paddle2.x + (self.paddle2.size[0]/2), self.paddle2.y + self.paddle2.size[1])
        paddle2_stred_nahore = (self.paddle2.x + (self.paddle2.size[0]/2), self.paddle2.y)
        paddle2_stred_leva = (self.paddle2.x, self.paddle2.y + (self.paddle2.size[1]/2))
        paddle2_stred_prava = (self.paddle2.x + self.paddle2.size[0], self.paddle2.y + (self.paddle2.size[1]/2))

        paddle1_stred_nahore = (self.paddle1.x + (self.paddle1.size[0]/2), self.paddle1.y)
        paddle1_stred_leva = (self.paddle1.x, self.paddle1.y + (self.paddle1.size[1]/2))
        paddle1_stred_prava = (self.paddle1.x + self.paddle1.size[0], self.paddle1.y + (self.paddle1.size[1]/2))
        paddle1_stred_dole = (self.paddle1.x + (self.paddle1.size[0]/2), self.paddle1.y + self.paddle1.size[1])

        # -------------------- DETEKCE DESEK ----------------------

        if (mic_stred_horni[1] <= paddle2_stred_dole[1]) and (mic_stred_spodni[1] > paddle2_stred_dole[1]) and \
                (mic_stred_prava[0] >= paddle2_stred_leva[0]) and (mic_stred_leva[0] < paddle2_stred_prava[0]):

            k = -(mic_stred_horni[0] - paddle2_stred_dole[0])
            self.reflectYupk(self.paddle2.y + self.paddle2.size[1],k)

        if (mic_stred_spodni[1] >= paddle1_stred_nahore[1]) and (mic_stred_horni[1] < paddle1_stred_nahore[1]) and \
                (mic_stred_prava[0] >= paddle1_stred_leva[0]) and (mic_stred_leva[0] < paddle1_stred_prava[0]):

            k = -(mic_stred_spodni[0] - paddle1_stred_nahore[0])
            self.reflectYdownk(self.paddle1.y,k)

        # -------------------- DETEKCE HRAN ----------------------

        if self.ball.x + self.ball.size[0] > self.prava:
            self.reflectXright(self.prava)

        if self.ball.x < self.leva:
            self.reflectXleft(self.leva)

        if self.ball.y < self.nahore:
            self.player.takes += 1
            self.player.StopTime()
            self.ballInGame = 0

        if self.ball.y > self.dole:
            self.player.takes += 1
            self.player.StopTime()
            self.ballInGame = 0

        if self.gone == 1:
            self.player.StopTime()
            self.ballInGame = 0
            self.player.SaveData()
            self.player.Respawn()
            self.generateBlocks()



    # -------------------------- ODRAZY ----------------------------
    def reflectYupk(self, yNew, k):
        d = -((((float(self.paddle2.size[0]/2))/100)*k)/100)
        dy = self.ball.y - yNew
        self.ball.stupen = self.ball.stupen - ((2+(d/2)) * self.ball.stupen)
        self.ball.uhel = math.radians(self.ball.stupen)
        self.ball.y = self.ball.y - 2 * dy

    def reflectYdownk(self, yNew, k):
        d = -((((float(self.paddle2.size[0]/2))/100)*k)/100)
        dy = self.ball.y + self.ball.size[1] - yNew
        self.ball.stupen = self.ball.stupen - ((2+(d/2)) * self.ball.stupen)
        self.ball.uhel = math.radians(self.ball.stupen)
        self.ball.y = self.ball.y - 2 * dy

    def reflectYup(self, yNew):
        dy = self.ball.y - yNew
        self.ball.stupen = self.ball.stupen - (2 * self.ball.stupen)
        self.ball.uhel = math.radians(self.ball.stupen)
        self.ball.y = self.ball.y - 2 * dy

    def reflectYdown(self, yNew):
        dy = self.ball.y + self.ball.size[1] - yNew
        self.ball.stupen = self.ball.stupen - (2*self.ball.stupen)
        self.ball.uhel = math.radians(self.ball.stupen)
        self.ball.y = self.ball.y - 2 * dy

    def reflectXright(self, xNew):
        dx = self.ball.x + self.ball.size[0] - xNew
        self.ball.stupen = (90 - self.ball.stupen) + 90
        self.ball.uhel = math.radians(self.ball.stupen)
        self.ball.x = self.ball.x - 2 * dx

    def reflectXleft(self, xNew):
        dx = self.ball.x - xNew
        self.ball.stupen = (90 - self.ball.stupen) + 90
        self.ball.uhel = math.radians(self.ball.stupen)
        self.ball.x = self.ball.x - 2 * dx

    def GenerateAngle(self):
        stupen = random.randint(30, 151)
        if (stupen <= 95) and (stupen >= 85):
            self.GenerateAngle()
        self.ball.stupen = - stupen
        self.ball.uhel = math.radians(- stupen)

    def isBallInGame(self):
        return self.ballInGame

    def setBallInGame(self, ballInGame):
        self.player.StartTime()
        self.ballInGame = ballInGame



class Player:
    def __init__(self):
        self.name = None
        self.points = 0
        self.takes = 0
        self.time = 0
        self.cistycas = 0
        self.TimeListStart = []
        self.TimeListStop = []

    def GenerateName(self):
        name = time.strftime("%y%m%d%H%M%S")
        self.name = name
        print 'New player: ', name

    def Respawn(self):
        self.points = 0
        self.takes = 0
        self.time = 0
        self.cistycas = 0
        self.TimeListStart = []
        self.TimeListStop = []

    def StartTime(self):
        self.start = time.time()
        self.TimeListStart.append(self.start)

    def StopTime(self):
        self.stop = time.time()
        self.TimeListStop.append(self.stop)

    def Count(self):
        mezicas = 0
        for i in range(len(self.TimeListStart)):
            start = self.TimeListStart[i]
            stop = self.TimeListStop[i]
            mezicas = mezicas + (stop - start)
        self.cistycas = round(mezicas, 2)

    def SaveData(self):
        self.Count()
        data = {'nick': self.name, 'takes': self.takes, 'points': self.points, 'time': self.cistycas}
        soubor = file('score.config', 'a+')
        yaml.dump(data, soubor)


# Třída pro herní desku
class Paddle:
    def __init__(self,size = (100, 20),x = 0, y = 0, t = 0):
        self.size = size
        self.x = x
        self.y = y
        self.t = t
    
# Třída pro micek
class Ball:
    def __init__(self,speed=300,size = (20, 20),x = 0,y = 0,xn = 0,yn = 0,xp = 0,yp = 0,uhel = 0,stupen = -45):
        self.speed = speed
        self.size = size
        self.x = x
        self.y = y
        self.xn = xn
        self.yn = yn
        self.xp = xp
        self.yp = yp
        self.uhel = uhel
        self.stupen = stupen
        
