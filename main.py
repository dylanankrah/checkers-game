# -*- coding: utf-8 -*-
# -*- Boucle principale -*-

# Librairies

import numpy as np
import pygame
from util import NeighborCells, AllColored, DisplayMessage

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

# Création de la grille et des états

grid = np.zeros((DIM_GRID,DIM_GRID))
gridStates = [np.zeros((DIM_GRID,DIM_GRID))] # États de jeu (pour revenir en arrière)

# Initialisation

pygame.init()
screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Jeu de dames")

# --- Boucle principale ---

# Nombre de dames placées
dCount = 0
# Nombre de cases blanches
cCount = DIM_GRID**2
# Numéro du tour actuel joué (correspondant au nombre de dames posées effectivement)
currentNum = 0

DONE = False # True lorsque le joueur décide de fermer la fenêtre
clock = pygame.time.Clock() # utile pour le taux d'images par seconde
            
while not DONE:
    
    for event in pygame.event.get(): # dès que le joueur fait une action
        
        if event.type == pygame.QUIT: # s'il s'agit de quitter le jeu
            
            DONE = True
            
        elif event.type == pygame.MOUSEBUTTONDOWN: # sinon s'il clique dans la fenêtre
            
            # Couleur d'arrière-plan | permet l'actualisation du message (voir suite)
            screen.fill(BLACK)
            
            # Dessin du bouton précédent
            
            previousButton = pygame.transform.scale(pygame.image.load('precedent.png'), (50,50))
            screen.blit(previousButton, previousButton.get_rect(center=(25,DIM_GRID*(HEIGHT + MARGIN) + 25)))
            
            pos = pygame.mouse.get_pos() # on récupère la position du clic
            
            if pos[1] > DIM_GRID*(HEIGHT+MARGIN) and pos[0] < 50: # si ça demande précédent (on place le bouton précédent tout en bas à gauche)
                
                if currentNum != 0:
                    currentNum -= 1 # on recule d'un tour
                    dCount -= 1 # on retire alors une dame
                
                    del gridStates[-1] # on supprime l'état le plus récent
                    grid = np.copy(gridStates[currentNum]) # et on passe au précédent
                
                if DEBUG_MODE:
                    print("précédent, currentNum: ", currentNum)
            
            else: # sinon ça poursuit
                
                column, row = pos[0] // (WIDTH + MARGIN), pos[1] // (HEIGHT + MARGIN) # et on en déduit la case correspondante
                neighbors = NeighborCells(row, column, DIM_GRID) # on trouve ensuite les cases sur les même ligne, colonne et diagonales
            
                if DEBUG_MODE: # utile pour le debugging
                    print("Click ", pos, "Coord: ", row, column)
                    print(neighbors)
              
                if grid[row][column] == 1 or grid[row][column] == 2: # si la case est déjà colorée, on envoie un message
                    DisplayMessage("Déjà colorée", screen, (WINSIZE[0]/2, WINSIZE[1]-25))
                
                if grid[row][column] == 0: # sinon la case passe à l'état "cliquée"
                    currentNum += 1 # on joue donc un tour
                    grid[row][column] = 1 # juste ici
                    dCount += 1 # une dame de plus
                    DisplayMessage("", screen, (WINSIZE[0]/2, WINSIZE[1]-25))
                
                    for cell in neighbors: 
                        if grid[cell[0]][cell[1]] == 0:
                            grid[cell[0]][cell[1]] = 2 # chaque case associée devient ainsi rouge
                            
                    gridStates.append(np.copy(grid)) # on ajoute le nouvel état de jeu à la liste des états
                        
                if DEBUG_MODE:
                    print("num. placées: ", dCount)
                    
            if DEBUG_MODE:
                print("grid: ", grid)
                print("gridStates: ", gridStates)
                print("currentNum: ", currentNum)
                
        # CONDITIONS D'ARRÊT 
        
            if dCount == DIM_GRID: # lorsque le joueur parvient à placer les N dames
                DisplayMessage("Félicitations!", screen, (WINSIZE[0]/2, WINSIZE[1]-25))
            
            if dCount < DIM_GRID and AllColored(grid): # lorsque toutes les cases sont colorées
                DisplayMessage("Perdu...", screen, (WINSIZE[0]/2, WINSIZE[1]-25))
            
    # Dessin de la grille
    
        for row in range(DIM_GRID):
            for column in range(DIM_GRID):
                if grid[row][column] == 0: # 0: état de base
                    pygame.draw.rect(screen, WHITE, [(MARGIN + WIDTH)*column + MARGIN, (MARGIN + HEIGHT)*row + MARGIN, WIDTH, HEIGHT]) # on dessine le rectangle de couleur correspondante dans la case
                
                if grid[row][column] == 1: # 1: cliqué
                    pygame.draw.rect(screen, BROWN, [(MARGIN + WIDTH)*column + MARGIN, (MARGIN + HEIGHT)*row + MARGIN, WIDTH, HEIGHT]) # on dessine le rectangle de couleur correspondante dans la case
                    # dessin de la dame
                    img = pygame.transform.scale(pygame.image.load('dame.png'), (WIDTH,HEIGHT))
                    screen.blit(img, img.get_rect(center=((MARGIN + WIDTH)*column + MARGIN + WIDTH/2,(MARGIN + HEIGHT)*row + MARGIN + HEIGHT/2)))
                
                if grid[row][column] == 2: # 2: case éliminée
                    pygame.draw.rect(screen, RED, [(MARGIN + WIDTH)*column + MARGIN, (MARGIN + HEIGHT)*row + MARGIN, WIDTH, HEIGHT]) # on dessine le rectangle de couleur correspondante dans la case
                
    
    clock.tick(60) # taux d'images par seconde
    
    pygame.display.flip() # actualisation de l'écran
    
# Fin de jeu
pygame.quit()
