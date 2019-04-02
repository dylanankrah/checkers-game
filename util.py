# -*- coding: utf-8 -*-
# -*- Fonctions utiles -*-

import pygame

def NeighborCells(row, column, dimGrid): # renvoie, pour une case, la liste des cases sur les mêmes ligne, colonne et diagonales
    neighborCells = []
    
    for i in range(0,row):
        neighborCells.append([i,column])
        
    for i in range(row + 1, dimGrid):
        neighborCells.append([i,column])
        
    for i in range(0,column):
        neighborCells.append([row,i])
    
    for i in range(column + 1, dimGrid):
        neighborCells.append([row,i])
        
    i,j = row,column
    while (i > 0 and j > 0):
        i -= 1
        j -= 1
        neighborCells.append([i,j])
        
    i,j = row,column
    while (i < dimGrid - 1 and j < dimGrid - 1):
        i += 1
        j += 1
        neighborCells.append([i,j])
    
    i,j = row,column
    while (i > 0 and j < dimGrid - 1):
        i -= 1
        j += 1
        neighborCells.append([i,j])    
        
    i,j = row,column
    while (i < dimGrid - 1 and j > 0):
        i += 1
        j -= 1
        neighborCells.append([i,j])    
        
    return neighborCells

def WriteMessage(message): # renvoie un texte affichable
    
    pygame.font.init()
    usedFont = pygame.font.SysFont('Arial', 18)
    
    textSurface = usedFont.render(message, True, (255,255,255)) # couleur blanche, antialiasing activé
    
    return(textSurface)
    
def AllColored(grid): # retourne True si une grille est totalement colorée
    (m,n) = grid.shape
    for k in range(m):
        for j in range(n):
            if grid[k,j] == 0:
                return False
    
    return True

def DisplayMessage(msg, screen, ctr):
    message = WriteMessage(msg)
    screen.blit(message, message.get_rect(center=ctr))