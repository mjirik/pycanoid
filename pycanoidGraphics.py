#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import pickle
import yaml
import numpy as np

class GameGraphics:
    def __init__(self,game,velikost_okna = (1024, 768)):

        # self.rows = 10
        # self.cols = 30

        # self.seznam = []

        self.game = game
        self.velikost_okna = velikost_okna
        # BARVY
        self.bila = 250, 250, 250
        self.cerna = 0, 0, 0
        self.zelena = 0, 250, 0
        self.modra = 0, 0, 250

        # Rozměry
        self.odsazeni = int(self.velikost_okna[0] / 6.8)
        self.odsazeni_dole = int(self.velikost_okna[1] / 13.6)
        self.herni_velikost = (self.velikost_okna[0] - (self.odsazeni * 2), self.velikost_okna[1] - self.odsazeni_dole) # velikost plochy kde létá kulička

        # Výpočty okrajů pro hraní
        self.horni_levy = ((self.velikost_okna[0] - self.herni_velikost[0]) / 2, 0)
        self.horni_pravy = (self.horni_levy[0] + self.herni_velikost[0], self.horni_levy[1])
        self.spodni_levy = (self.horni_levy[0], self.herni_velikost[1])
        self.spodni_pravy = (self.horni_pravy[0], self.herni_velikost[1])

        # Mys
        pygame.mouse.set_visible(0)

        # Pismo
        self.pismo = pygame.font.Font('freesansbold.ttf', 20)

        # Inicializace okna
        self.obrazovka = pygame.display.set_mode(self.velikost_okna)
        pygame.display.set_caption('Pycanoid')

        # Surface pro kreslení všeho vzadu
        self.pozadi = pygame.Surface(self.velikost_okna)
        self.pozadi.fill(self.cerna)

        # Surfce pro blok
        self.block_surface = pygame.Surface(self.GetBlockSize())
        self.block_surface.fill(self.bila)

        # Surface pro desku
        self.deska_surface = pygame.Surface(self.game.paddle1.size)
        self.deska_surface.fill(self.zelena)
        self.deska_surface = pygame.image.load("grafika/paddledown.png")#HOLI

       # Surface pro kuličku
        self.ball_surface = pygame.Surface(self.game.ball.size)

        #ball_surface.fill(bila)
        #self.ball_surface = pygame.image.load("grafika/ball.png")#HOLI

        # Výpočty okrajů pro hraní
        self.horni_levy = ((self.velikost_okna[0] - self.herni_velikost[0]) / 2, 0)
        self.horni_pravy = (self.horni_levy[0] + self.herni_velikost[0], self.horni_levy[1])
        self.spodni_levy = (self.horni_levy[0], self.herni_velikost[1])
        self.spodni_pravy = (self.horni_pravy[0], self.herni_velikost[1])

        # Surface pro herni oblast HOLI
        self.oblast_surface = pygame.Surface((self.horni_pravy[0]-self.horni_levy[0]-1,self.spodni_levy[1]- self.horni_levy[1]-1))
        try:
            img_url = "grafika/test1.jpg"
            # img_url = ' http://webs.zcu.cz/kamery/kamera1.jpg'
            # img_url = 'http://kamera.plzen.cz/webcam.jpg?0.8093254372943193'
            # import urllib
            # import StringIO
            # f = StringIO.StringIO(urllib.urlopen(img_url).read())
            self.oblast_surface = pygame.image.load(f, 'cam.jpg')
        except:
            img_url = "grafika/test1.jpg"
            self.oblast_surface = pygame.image.load(img_url)


        # Surface pro vypis HOLI
        self.vypis_surfaceBall = pygame.Surface((300,200))
        self.vypis_surfaceBall.fill(self.cerna)
        self.vypis_surfaceDeska1 = pygame.Surface((200,200))
        self.vypis_surfaceDeska1.fill(self.cerna)

        self.prava = self.horni_pravy[0]  # X souřadnice pro pravou herní plochu
        self.leva = self.horni_levy[0]    # X souřadnice pro levou herní plochu
        self.nahore = self.horni_levy[1]  # Y souřadnice pro horní stranu
        self.dole = self.spodni_levy[1]   # Y souřadnice spodního kraje

        # Vykreslení okrajů
        pygame.draw.line(self.pozadi, self.bila, self.horni_levy, self.horni_pravy)
        pygame.draw.line(self.pozadi, self.bila, self.spodni_levy, self.spodni_pravy)
        pygame.draw.line(self.pozadi, self.bila, self.horni_levy, self.spodni_levy)
        pygame.draw.line(self.pozadi, self.bila, self.horni_pravy, self.spodni_pravy)


    def CreateBackground(self):
        """
    Tvoří základní pozadí, vše co je vidět
        """
        self.obrazovka.blit(self.pozadi, (0, 0))
        #HOLI
        self.obrazovka.blit(self.oblast_surface, (self.horni_levy[0]+1, self.horni_levy[1]+1))
        self.obrazovka.blit(self.vypis_surfaceBall, (10, self.dole+10))
        self.obrazovka.blit(self.vypis_surfaceDeska1, (400, self.dole+10))

    def DrawBallBegin(self):
        """
    Vykresluje kuličku na začátku hry
        """
        self.game.ball.x = (self.game.paddle1.x + self.game.paddle1.size[0] / 2) - (self.game.ball.size[0] / 2)
        self.game.ball.y = self.game.paddle1.y - self.game.ball.size[1]
        self.ball_rect_beg = pygame.Rect(self.game.ball.x,self.game.ball.y,self.game.ball.size[0],self.game.ball.size[1])
        pygame.draw.rect(self.obrazovka, (255,0,0), self.ball_rect_beg, 3)
        #self.obrazovka.blit(self.ball_surface, (self.game.ball.x, self.game.ball.y))

    def DrawBall(self,x,y):
        self.ball_rect = pygame.Rect(x,y,self.game.ball.size[0],self.game.ball.size[1])
        pygame.draw.rect(self.obrazovka, (255,0,0), self.ball_rect, 3)
        self.kolize = self.ball_rect.collidelist(self.seznam)
        if self.kolize != -1:
            k = self.kolize
            self.kolize_blok = self.seznam[k]
            self.detect_kol()
            self.destroy_blok(k)

    def destroy_blok(self,k):
        matrix = np.load('blockmap.npy')
        i = 0
        for r in range(matrix.shape[0]):
            for s in range(matrix.shape[1]):
                if matrix[r,s] == 1:
                    if i == k:
                        matrix[r,s] = 0
                        np.save('blockmap.npy', matrix)
                    i = i + 1

    def empty_matrix(self):
        if self.num_blocks == 0:
            return 1
        else:
            return 0

    def detect_kol(self):
        if self.kolize != -1:
            return self.kolize_blok

        else:
            return -1


    def DrawDesk(self,position, ddeska, ndeska = 0):
        """
    Kontrola spravneho umisteni odrazeci desky
    :param position:
        deska: objekt desky
        ndeska: 0 - dole, 1 - nahore
    """
        if ndeska == 0:
            deskay = self.herni_velikost[1] - ddeska.size[1]-10
        else:
            deskay = 10 # herni_velikost[1] - ddeska.size[1] - 30

        # podminka pro herni oblast
        if (position[0] - ddeska.size[0] / 2 >= self.spodni_levy[0]) and (position[0] + ddeska.size[0] / 2 <= self.spodni_pravy[0]):
            ddeska.x = position[0] - ddeska.size[0] / 2
            ddeska.y = deskay
            self.obrazovka.blit(self.deska_surface, (ddeska.x, ddeska.y))

        # oblast nalevo od herni plochy
        elif position[0] - ddeska.size[0] / 2 <= self.spodni_levy[0]:
            ddeska.x = self.spodni_levy[0]
            ddeska.y = deskay
            self.obrazovka.blit(self.deska_surface, (ddeska.x, ddeska.y))

        # oblast napravo od herni plochy
        elif position[0] - ddeska.size[0] / 2 >= self.spodni_levy[0]:
            ddeska.x = self.spodni_pravy[0] - ddeska.size[0]
            ddeska.y = deskay
            self.obrazovka.blit(self.deska_surface, (ddeska.x, ddeska.y))

    def GetBlockSize(self):
        """
     Spocita velikost bloku tak, aby zustalo misto na kazde
    strane ve velikosti jednoho bloku.
        """
        matrix = np.load('blockmap.npy')
        x = float(self.herni_velikost[0] / (matrix.shape[0] + 2))
        y = float(self.herni_velikost[1] / (matrix.shape[1] + 20))
        size = (round(x, 0), round(y, 0))
        return size

    def BlockArea(self):
        odstup = self.GetBlockSize()
        point = (self.horni_levy[0] + odstup[0], (self.spodni_levy[1]/3.5))
        point = (round(point[0], 0), round(point[1], 0))
        return point

    def DrawInformations(self,game):
        """
    Vykresluje ladící výpisy přímo do hry
        """
        text = "ball| x:" + str(round(game.ball.x)) + "| y:" + str(round(game.ball.y))
        self.vypis_surfaceBall = self.pismo.render(text,  1, self.modra, self.cerna)
        textDeska1 = "deska1 dolni|  x:" + str(round(game.paddle1.x))
        self.vypis_surfaceDeska1 = self.pismo.render(textDeska1,  1,self.modra, self.cerna)

    def DrawBlocks(self,point,size):
        matrix = np.load('blockmap.npy')
        originalx = point[0]

        self.seznam = []
        for r in range(matrix.shape[0]):
            for s in range(matrix.shape[1]):

                if matrix[r,s]:
                    box = pygame.Rect(point[0], point[1], size[0],size[1])
                    pygame.draw.rect(self.obrazovka, (255,255,0), box, 3)
                    blok = (point[0], point[0] + size[0], point[1], point[1] + size[1])    # (x1, x2, y1, y2)
                    self.seznam.append(box)
                point = (point[0] + size[0], point[1])
            point = (originalx, point[1] + size[1])
        self.num_blocks = len(self.seznam)