# -*- coding: utf-8 -*-
# -*- Boucle principale -*-

# Librairies

import numpy as np
import pygame
from gamelogic import NeighborCells, WriteMessage

# Couleurs et tailles

WHITE = (255,255,255)
RED = (255,0,0)
BROWN = (160,82,45)
BLACK = (0,0,0)

WIDTH, HEIGHT = 60,60 # taille d'une case
MARGIN = 2 # marge (ligne noire)

# Définition de la grille

DIM_GRID = int(input("N = ")) # N
DEBUG_MODE = input("Debug mode : ") # debug mode
WINSIZE = [(WIDTH + MARGIN)*DIM_GRID + MARGIN,(HEIGHT + MARGIN)*DIM_GRID + MARGIN + 50] # taille de la fenêtre de jeu (marge supp. de 50px en bas pour les messages et les boutons)

# Création de la grille

grid = np.zeros((DIM_GRID,DIM_GRID))

# Initialisation

pygame.init()
screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Jeu de dames")

# --- Boucle principale ---

# Nombre de dames placées
dCount = 0

# Nombre de cases blanches
cCount = DIM_GRID**2

# Voisinage vide au début du jeu
neighbors = []

DONE = False # True lorsque le joueur décide de fermer la fenêtre
clock = pygame.time.Clock() # utile pour le taux d'images par seconde
            
while not DONE:
    
    for event in pygame.event.get(): # dès que le joueur fait une action
        
        if event.type == pygame.QUIT: # s'il s'agit de quitter le jeu
            
            DONE = True
            
        elif event.type == pygame.MOUSEBUTTONDOWN: # sinon s'il clique dans la fenêtre
            
            # Couleur d'arrière-plan | permet l'actualisation du message (voir suite)
            screen.fill(BLACK)
    
            pos = pygame.mouse.get_pos() # on récupère la position du clic
            column, row = pos[0] // (WIDTH + MARGIN), pos[1] // (HEIGHT + MARGIN) # et on en déduit la case correspondante
            
            neighbors = NeighborCells(row, column, DIM_GRID) # on trouve ensuite les cases sur les même ligne, colonne et diagonales
            
            if DEBUG_MODE: # utile pour le debugging
                print("Click ", pos, "Coord: ", row, column)
                print(neighbors)
              
            if grid[row][column] == 1 or grid[row][column] == 2: # si la case est déjà colorée, on envoie un message
                errorMessage = WriteMessage("Déjà colorée!")
                screen.blit(errorMessage, errorMessage.get_rect(center=(WINSIZE[0]/2, WINSIZE[1]-25)))
                
            elif grid[row][column] == 0: # sinon la case passe à l'état "cliquée"
                grid[row][column] = 1
                dCount += 1 # une dame de plus
                cCount -= 1 # une case blanche en moins
                playMessage = WriteMessage("")
                screen.blit(playMessage, playMessage.get_rect(center=(WINSIZE[0]/2, WINSIZE[1]-25)))
                
                for cell in neighbors: 
                    if grid[cell[0]][cell[1]] == 0:
                        grid[cell[0]][cell[1]] = 2 # chaque case associée devient ainsi rouge
                        cCount -= 1 # une case blanchee en moins
                        
            if DEBUG_MODE:
                print("num. placées: ", dCount)
                print("num. cases restantes: ", cCount)
                
        # CONDITIONS D'ARRÊT 
        
        if dCount == DIM_GRID: # lorsque le joueur parvient à placer les N dames
            winMessage = WriteMessage("Félicitations!")
            screen.blit(winMessage, winMessage.get_rect(center=(WINSIZE[0]/2, WINSIZE[1]-25)))
            
        if dCount < DIM_GRID and cCount == 0: # lorsque toutes les cases sont colorées
            lossMessage = WriteMessage("Perdu...")
            screen.blit(lossMessage, lossMessage.get_rect(center=(WINSIZE[0]/2, WINSIZE[1]-25)))
            
    # Dessin de la grille
    
    for row in range(DIM_GRID):
        for column in range(DIM_GRID):
            
            if grid[row][column] == 0:
                color = WHITE # 0: état de base
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH)*column + MARGIN, (MARGIN + HEIGHT)*row + MARGIN, WIDTH, HEIGHT]) # on dessine le rectangle de couleur correspondante dans la case
                
            if grid[row][column] == 1:
                color = BROWN # 1: cliqué
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH)*column + MARGIN, (MARGIN + HEIGHT)*row + MARGIN, WIDTH, HEIGHT]) # on dessine le rectangle de couleur correspondante dans la case
                # dessin de la dame
                img = pygame.transform.scale(pygame.image.load('dame.bmp'), (WIDTH,HEIGHT))
                
                screen.blit(img, img.get_rect(center=((MARGIN + WIDTH)*column + MARGIN + WIDTH/2,(MARGIN + HEIGHT)*row + MARGIN + HEIGHT/2)))
                
            if grid[row][column] == 2:
                color = RED # 2: case éliminée
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH)*column + MARGIN, (MARGIN + HEIGHT)*row + MARGIN, WIDTH, HEIGHT]) # on dessine le rectangle de couleur correspondante dans la case
                
    
    clock.tick(60) # taux d'images par seconde
    
    pygame.display.flip() # actualisation de l'écran
    
# Fin de jeu
pygame.quit()
