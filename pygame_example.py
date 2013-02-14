# -*- coding: utf-8 -*-                             # utf-8 kódování zdrojového kódu
 
import pygame                                       # import modulu Pygame
pygame.init()                                       # inicializace modulu
 
screen = pygame.display.set_mode((640,480))         # vytvoření okna s nastavením jeho velikosti
pygame.display.set_caption("Example")               # nastavení titulku okna
 
background = pygame.Surface(screen.get_size())      # vytvoření vrstvy pozadí
background = background.convert()                   # převod vrstvy do vhodného formátu
background.fill((0,0,255))                          # obarvení vrstvy modře (r, g, b – červená, zelená, modrá)
 
basicFont = pygame.font.SysFont(None, 64)           # načtení písma velikosti 64
text = basicFont.render('Hello world!', True, (0, 255, 0))
                                 # vytvoření vrstvy s textem "Hello world!", zapnuté vyhlazování, zelené písmo
textRect = text.get_rect()                          # získání pozic vrstvy textu
textRect.centerx = screen.get_rect().centerx        # nastavení pozice x textu na střed obrazovky
textRect.centery = screen.get_rect().centery        # nastavení pozice y textu na střed obrazovky
 
clock = pygame.time.Clock()                         # časování
keepGoing = True                                    # podmínka pro hlavní smyčku
 
while keepGoing:                                    # hlavní smyčka
    clock.tick(30)                                  # omezení maximálního počtu snímků za sekundu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               # probíhá událost požadující zavření okna programu?
            keepGoing = False                       # ukončení hlavní smyčky
 
    screen.blit(background, (0,0))                  # přidání pozadí k vykreslení na pozici 0, 0
    screen.blit(text, textRect)                     # přidání textu k vykreslení na střed
    pygame.display.flip()                           # vykreslení celého obrazu