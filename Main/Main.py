import pygame
# definice
bila = 250,250,250
cerna = 0,0,0
velikost_okna = (800,600)
herni_velikost = (600,500)
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# inicializace okna
obrazovka = pygame.display.set_mode(velikost_okna)
pozadi = pygame.Surface((velikost_okna))
pozadi.fill(cerna)
pygame.display.set_caption('Pycanoid')


surf1 = pygame.Surface((200,200))
pygame.draw.circle(surf1,bila, (100,100), 50, 2)


# okraje pro hrani
horni_levy = ((velikost_okna[0]-herni_velikost[0])/2, 0)
horni_pravy = (horni_levy[0]+herni_velikost[0], horni_levy[1])
spodni_levy = (horni_levy[0], herni_velikost[1])
spodni_pravy = (horni_pravy[0], herni_velikost[1])

pygame.draw.line(pozadi, bila, horni_levy,horni_pravy);
pygame.draw.line(pozadi, bila, spodni_levy,spodni_pravy);
pygame.draw.line(pozadi, bila, horni_levy,spodni_levy);
pygame.draw.line(pozadi, bila, horni_pravy,spodni_pravy);

# vykresleni na obraz
pygame.display.update()


# vykresleni testovaciho kruhu
def kresli_kruh(pozice_mysi):
    return pygame.draw.circle(obrazovka,bila, (pozice_mysi[0],herni_velikost[1]-50), 50, 2)
    
# cyklus hry
running = 1
while running:
    pozice_mysi = pygame.mouse.get_pos()
    #kresli_kruh(pozice_mysi)
    obrazovka.blit(pozadi,(0,0))
    obrazovka.blit(surf1,pozice_mysi)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
    pygame.display.update()


        
   
