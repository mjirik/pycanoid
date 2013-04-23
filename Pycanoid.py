#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time
import math
import random
pygame.init()


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

    def move(self, dt):
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


def DrawDesk(position):
    """
Kontrola spravneho umisteni odrazeci desky
:param position:
"""
    # podminka pro herni oblast
    if (position[0] - deska.size[0] / 2 >= spodni_levy[0]) and (position[0] + deska.size[0] / 2 <= spodni_pravy[0]):
        deska.x = position[0] - deska.size[0] / 2
        deska.y = herni_velikost[1] - deska.size[1]
        obrazovka.blit(deska_surface, (deska.x, deska.y))

    # oblast nalevo od herni plochy
    elif position[0] - deska.size[0] / 2 <= spodni_levy[0]:
        deska.x = spodni_levy[0]
        deska.y = herni_velikost[1] - deska.size[1]
        obrazovka.blit(deska_surface, (deska.x, deska.y))

    # oblast napravo od herni plochy
    elif position[0] - deska.size[0] / 2 >= spodni_levy[0]:
        deska.x = spodni_pravy[0] - deska.size[0]
        deska.y = herni_velikost[1] - deska.size[1]
        obrazovka.blit(deska_surface, (deska.x, deska.y))


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


# Inicializace tříd
deska = DESKA
ball = BALL()

# BARVY
bila = 250, 250, 250
cerna = 0, 0, 0
zelena = 0, 250, 0
modra = 0, 0, 250

# Rozměry
velikost_okna = (1024, 768)                                               # okno které se zobrazuje po spuštění
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


pygame.display.update()


running = 1
click = 0
lives = 3

while running:
        CreateBackground()
        m_pos = pygame.mouse.get_pos()    # aktuální pozice myši
        DrawDesk(m_pos)

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

        pygame.display.update()
        fpsClock.tick(FPS)