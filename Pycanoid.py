#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time
import math
import random
#import pickle
import yaml
import os
import facecontrol


defaut_parameters = {
        'ip_server':'192.168.1.5', 
        'host':True,
        'nplayers':2,
        'control1':'mouse',
        'window_size':(1024,768)
        }
pygame.init()

def comunication_init(parameters):
# Místo pro inicializaci síťové komunikace
# Asi by se zde mělo rozhodovat, kdo bude player1 a kdo bude player2
    comunication_parameters = None
    return comunication_parameters

def comunication_loop(game_state, comunication_parameters):
# Tato funkce je volána v každé smyčce aplikace. 
    return game_state

    pass


def get_parameters():
    """
    Funkce obstará základní parametry
    """
    config_file = 'pycanoid.config'
    if os.path.isfile(config_file):
        stream = file(config_file, 'r')    # 'document.yaml' contains a single YAML document.
        parameters = defaut_parameters
        parameters.update(yaml.load(stream))
    else:
        parameters = defaut_parameters
        with open(config_file, 'wb') as f:
            yaml.dump(parameters, f)

    return parameters


def mux_game_state(deska1, deska2, ball):
    gs = {
            'player1':{'x':deska1.x, 'y':deska1.y, 'z':0, 'name':'Jednicka'},
            'player2':{'x':deska2.x, 'y':deska2.y, 'z':0, 'name':'Dvojka'},
            'ball':{'x':ball.x,'y':ball.y},
            'gamefield':{'zatim':'nic'}
            }

    return gs

def demux_game_state(gs, deska1, deska2, ball):
    deska1.x = gs['player1']['x']
    deska1.y = gs['player1']['y']
    deska2.x = gs['player2']['x']
    deska2.y = gs['player2']['y']

    ball.x = gs['ball']['x']
    ball.y = gs['ball']['y']
    return deska1, deska2, ball



# Třída pro herní desku
class DESKA:
    t = 0
    x = 0
    y = 0
    size = (100, 20)


# Třída pro "míč"
class BALL:
    x = 0
    y = 0
    xn = 0
    yn = 0
    xp = 0
    yp = 0
    stupen = -45
    uhel = 0 # math.radians(stupen)
    speed = 500
    size = (20, 20)

    def move(self, dt ):
        dx = math.cos(self.uhel) * self.speed * dt   # Výpočet příštích souřadnic x,y
        dy = math.sin(self.uhel) * self.speed * dt

        self.xp = self.x                        # Posunutí aktuálních souřadnic do předchozích
        self.yp = self.y

        self.x += dx                   # Výpočet nových souřadnic s kompenzací času
        self.y += dy

        if self.x + self.size[0] > prava:
            self.reflectXright(prava)

        if self.x < leva:
            self.reflectXleft(leva)

        if self.y < nahore:
            self.reflectYup(nahore)

        if (self.y + self.size[1] > deska.y) and ((self.x >= deska.x) and (self.x + self.size[0]) <= (deska.x + deska.size[0])):
            self.reflectYdown(deska.y)

        if self.y > dole:
            global click, lives
            lives -= 1
            click = 0

    def reflectYup(self, y):
        dy = self.y - y
        self.stupen = self.stupen - (2*self.stupen)
        self.uhel = math.radians(self.stupen)
        self.y = self.y - 2 * dy

    def reflectYdown(self, y):
        dy = self.y + self.size[1] - y
        self.stupen = self.stupen - (2*self.stupen)
        self.uhel = math.radians(self.stupen)
        self.y = self.y - 2 * dy

    def reflectXright(self, x):
        dx = self.x + self.size[0] - x
        self.stupen = (90 - self.stupen) + 90
        self.uhel = math.radians(self.stupen)
        self.x = self.x - 2 * dx

    def reflectXleft(self, x):
        dx = self.x - x
        self.stupen = (90 - self.stupen) + 90
        self.uhel = math.radians(self.stupen)
        self.x = self.x - 2 * dx


def CreateBackground():
    """
Tvoří základní pozadí, vše co je vidět

    """
    obrazovka.blit(pozadi, (0, 0))


def DrawDesk(position, ddeska, ndeska = 0):
    """
Kontrola spravneho umisteni odrazeci desky
:param position:
    deska: objekt desky
    ndeska: 0 - dole, 1 - nahore
"""
    if ndeska == 0:
        deskay = herni_velikost[1] - ddeska.size[1]
    else:
        deskay = 30 # herni_velikost[1] - ddeska.size[1] - 30

    # podminka pro herni oblast
    if (position[0] - ddeska.size[0] / 2 >= spodni_levy[0]) and (position[0] + ddeska.size[0] / 2 <= spodni_pravy[0]):
        ddeska.x = position[0] - ddeska.size[0] / 2
        ddeska.y = deskay
        obrazovka.blit(deska_surface, (ddeska.x, ddeska.y))

    # oblast nalevo od herni plochy
    elif position[0] - deska.size[0] / 2 <= spodni_levy[0]:
        ddeska.x = spodni_levy[0]
        ddeska.y = deskay
        obrazovka.blit(deska_surface, (ddeska.x, ddeska.y))

    # oblast napravo od herni plochy
    elif position[0] - deska.size[0] / 2 >= spodni_levy[0]:
        ddeska.x = spodni_pravy[0] - ddeska.size[0]
        ddeska.y = deskay
        obrazovka.blit(deska_surface, (ddeska.x, ddeska.y))


def DrawBallBegin():
    """
Vykresluje kuličku na začátku hry
    """
    ball.x = (deska.x + deska.size[0] / 2) - (ball.size[0] / 2)
    ball.y = deska.y - ball.size[1]
    obrazovka.blit(ball_surface, (ball.x, ball.y))


def GenerateAngle():
    stupen = random.randint(10, 171)
    if stupen == -90:
        GenerateAngle()
    ball.stupen = - stupen
    ball.uhel = math.radians(- stupen)

#def pycanoid():

print "Deprecated interface file. New is pycanoidMain.py"

parameters = get_parameters()

comunication_parameters = comunication_init(parameters)
# Inicializace tříd
deska = DESKA()
deska2 = None
ball = BALL()
if parameters['nplayers'] > 1:
    deska2 = DESKA()
    

# BARVY
bila = 250, 250, 250
cerna = 0, 0, 0
zelena = 0, 250, 0
modra = 0, 0, 250

# Rozměry
velikost_okna = parameters['window_size']
odsazeni = int(velikost_okna[0] / 6.8)
odsazeni_dole = int(velikost_okna[1] / 13.6)
herni_velikost = (velikost_okna[0] - (odsazeni * 2), velikost_okna[1] - odsazeni_dole)          # velikost plochy kde létá kulička

# Mys
pygame.mouse.set_visible(0)

# Pismo
pismo = pygame.font.Font('freesansbold.ttf', 25)

# Nastaveni FPS
FPS = 60
fpsClock = pygame.time.Clock()

# Inicializace okna
obrazovka = pygame.display.set_mode(velikost_okna)
pygame.display.set_caption('Pycanoid')

# Surface pro kreslení všeho vzadu
pozadi = pygame.Surface(velikost_okna)
pozadi.fill(cerna)

# Surface pro odrážecí desku
deska_surface = pygame.Surface(deska.size)
deska_surface.fill(bila)


# Surface pro kuličku
ball_surface = pygame.Surface(ball.size)
ball_surface.fill(bila)


# Výpočty okrajů pro hrání
horni_levy = ((velikost_okna[0] - herni_velikost[0]) / 2, 0)
horni_pravy = (horni_levy[0] + herni_velikost[0], horni_levy[1])
spodni_levy = (horni_levy[0], herni_velikost[1])
spodni_pravy = (horni_pravy[0], herni_velikost[1])

prava = horni_pravy[0]  # X souřadnice pro pravou herní plochu
leva = horni_levy[0]    # X souřadnice pro levou herní plochu
nahore = horni_levy[1]  # Y souřadnice pro horní stranu
dole = spodni_levy[1]   # Y souřadnice spodního kraje


# Vykreslení okrajů
pygame.draw.line(pozadi, bila, horni_levy, horni_pravy)
pygame.draw.line(pozadi, bila, spodni_levy, spodni_pravy)
pygame.draw.line(pozadi, bila, horni_levy, spodni_levy)
pygame.draw.line(pozadi, bila, horni_pravy, spodni_pravy)

if parameters['control1'] == 'face':
    fctrl = facecontrol.Facecontrol()

if parameters['nplayers'] > 1:
    game_state = mux_game_state(deska, deska2, ball)

pygame.display.update()


running = 1
click = 0
lives = 3



while running:
        CreateBackground()
        if parameters['control1'] == 'mouse':
            m_pos = pygame.mouse.get_pos()    # aktuální pozice myši
        elif parameters['control1'] == 'face':
            m_pos = fctrl.get_pos()
        DrawDesk(m_pos, deska)
        if parameters['nplayers'] > 1:
            DrawDesk([game_state['player2']['x'], game_state['player2']['y']] , deska2, 1)

        # Začátek hry
        if click == 0:
            GenerateAngle()
            DrawBallBegin()

        # Akce start
        elif click == 1:
            prev_time = actual_time
            actual_time = time.time()
            dt = actual_time - prev_time
            ball.move(dt)
            obrazovka.blit(ball_surface, (ball.x, ball.y))

        # Kontrola provedených akcí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # Ukončení aplikace stisknutím křížku
                running = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Aktivace tlačítka na myši
                click = 1
                prev_time = time.time()
                actual_time = time.time()


        # synchronizace po síti
        if parameters['nplayers'] > 1:
            game_state = mux_game_state(deska, deska2, ball)
            game_state = comunication_loop(game_state, comunication_parameters)
            deska, deska2, ball = demux_game_state(game_state, deska, deska2, ball)

        pygame.display.update()
        fpsClock.tick(FPS)


#if __name__ == "__main__":
#    pycanoid()
