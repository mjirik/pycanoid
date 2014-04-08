#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import time
import math
import random
#import pickle
import yaml
import os
import numpy as np

pygame.init()

class GameLogic:
    def __init__(self,parameters):
        #self.generateBlocks()
        self.parameters = parameters
        self.lives = 3
        self.part = 3
        self.ballInGame = 0 # 1-ball is in game, 0- somebody has lost the ball or begining 
        self.paddle1 = Paddle()
        if parameters['nplayers'] == 2:
            self.paddle2 = Paddle()
        self.ball = Ball()
        self.leva_horni  = (self.ball.x, self.ball.y)
        self.leva_spodni  = (self.ball.x, self.ball.y + self.ball.size[1])
        self.prava_spodni  = (self.ball.x + self.ball.size[0], self.ball.y + self.ball.size[1])
        self.prava_horni  = (self.ball.x + self.ball.size[0], self.ball.y)
        self.kolize_blok = -1

    def setkolize(self, blok):
        self.kolize_blok = blok

    def generateBlocks(self):
        """
        Generuje pokazde nahodne bloky pro hru
        """
        matrix = np.random.randint(2, size=(10, 10))
        np.save('blockmap', matrix)
        
    def setCorners(self,prava,leva,nahore,dole):
        self.prava = prava  # X souřadnice pro pravou herní plochu
        self.leva = leva    # X souřadnice pro levou herní plochu
        self.nahore = nahore  # Y souřadnice pro horní stranu
        self.dole = dole   # Y souřadnice spodního kraje

    def hit(self, n):
        matrix = np.load('blockmap.npy')
        tvar = matrix.shape
        k = 0
        run = True
        for r in range(tvar[0]):
            for s in range(tvar[1]):
                if matrix[r,s]:
                    k = k + 1
                    if k == n:
                        matrix[r,s] = 0
                        run = False
                        break
            if not run:
                break
        np.save('blockmap.npy', matrix)


    def moveBall(self, dt):
        dx = math.cos(self.ball.uhel) * self.ball.speed * dt   # Výpočet příštích souřadnic x,y
        dy = math.sin(self.ball.uhel) * self.ball.speed * dt

        self.ball.xp = self.ball.x                        # Posunutí aktuálních souřadnic do předchozích
        self.ball.yp = self.ball.y

        self.ball.x += dx                   # Výpočet nových souřadnic s kompenzací času
        self.ball.y += dy

        self.ball.x = self.ball.x
        self.ball.y = self.ball.y

        if self.kolize_blok != -1:  # doslo ke kolizi
            mic_stred_prava = (self.ball.x+self.ball.size[0], self.ball.y+(self.ball.size[1]/2))
            deska_stred_leva = (self.kolize_blok[0], self.kolize_blok[1]+(self.kolize_blok[3]/2))
            mic_stred_leva = (self.ball.x, self.ball.y+(self.ball.size[1]/2))
            deska_stred_prava = (self.kolize_blok[0]+self.kolize_blok[2], self.kolize_blok[1]+(self.kolize_blok[3]/2))
            mic_stred_horni = (self.ball.x+(self.ball.size[0]/2), self.ball.y)
            deska_stred_spodni = (self.kolize_blok[0]+(self.kolize_blok[2]/2), self.kolize_blok[1]+self.kolize_blok[3])
            mic_stred_spodni = (self.ball.x+(self.ball.size[0]/2), self.ball.y+self.ball.size[1])
            deska_stred_horni = (self.kolize_blok[0]+(self.kolize_blok[2]/2),self.kolize_blok[1])


            if (mic_stred_prava[0] >= deska_stred_leva[0]) and (mic_stred_leva[0] < deska_stred_leva[0]):
                self.reflectXright(self.kolize_blok[0])
            elif (mic_stred_leva[0] >= deska_stred_prava[0]) and (mic_stred_prava[0] > deska_stred_prava[0]):
                self.reflectXleft(self.kolize_blok[0]+self.kolize_blok[2])
            elif (mic_stred_horni[1] <= deska_stred_spodni[1]) and (mic_stred_spodni[1] > deska_stred_spodni[1]):
                self.reflectYup(self.kolize_blok[1]+self.kolize_blok[3])
            elif (mic_stred_spodni[1] >= deska_stred_horni[1]) and (mic_stred_horni[1] < deska_stred_horni[1]):
                self.reflectYdown(self.kolize_blok[1])


        # ---------------- DETEKCE HRAN -------------------

        if self.ball.x + self.ball.size[0] > self.prava:
            self.reflectXright(self.prava)

        if self.ball.x < self.leva:
            self.reflectXleft(self.leva)

        if self.ball.y < self.nahore:
            self.lives -= 1
            self.ballInGame = 0

        if self.ball.y > self.dole:
            self.lives -= 1
            self.ballInGame = 0

        #--------------- DETEKCE DESEK ---------------------

        if (self.ball.y < self.paddle2.y + self.paddle2.size[1]) and ((self.ball.x >= self.paddle2.x) and (self.ball.x + self.ball.size[0]) <= (self.paddle2.x + self.paddle2.size[0])):
            self.reflectYup(self.paddle2.y + self.paddle2.size[1])

        if (self.ball.y + self.ball.size[1] > self.paddle1.y) and ((self.ball.x >= self.paddle1.x) and (self.ball.x + self.ball.size[0]) <= (self.paddle1.x + self.paddle1.size[0])):
            self.reflectYdown(self.paddle1.y)


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
        stupen = random.randint(10, 171)
        if stupen == -90:
            self.GenerateAngle()
        self.ball.stupen = - stupen
        self.ball.uhel = math.radians(- stupen)

    def isBallInGame(self):
        return self.ballInGame

    def setBallInGame(self, ballInGame):
        self.ballInGame = ballInGame


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
        
