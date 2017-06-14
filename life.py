#This is the game of life

import pygame
import random
import time
import numpy as np
import math

black =         [0, 0, 0        ]
white =         [255, 255, 255  ]
green  =        [0, 255, 0      ]
red =           [255, 0, 0      ]
blue =          [0, 0, 255      ]
yellow =        [255, 255, 0    ]
pink =          [255, 0, 127    ]
orange =        [255, 128, 0    ]
purple =        [102, 0, 204    ]


pygame.init()

height = 10
width = 10
margin = 1

iso = 1
ovrc = 4
gen = 3

speed = 5.0
inc = 1.0

numrows = 10
numcols = 10

sizevert = margin + ((margin + height) * numrows)
sizehorz = margin + ((margin + width) * numcols)

size = [sizehorz, sizevert]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("The Game of Life")

clock = pygame.time.Clock()

def grid_init_blank():
    grid = np.zeros((numrows,numcols))
    return grid

def grid_init_rand():
    grid = np.random.random((numrows,numcols))
    return grid

def get_neighbors(grid,x,y):
    nbrs = grid[max(0,x-1):min(numrows,x+2),max(0,y-1):min(numcols,y+2)]
    total = np.sum(nbrs) - grid[x][y]
    return total

def step(x,n):
    if(x==0):
        if(n==gen):
            return 1
    elif(x==1):
        if((n>iso) & (n<ovrc)):
            return 1
    else:
        return -1
    return 0

grid = grid_init_blank()
gridaux = grid_init_blank()

done = False
play = False

while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid[x][y] = (grid[x][y]+1)%2
            get_neighbors(grid,x,y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_UP:
                speed = speed+inc
                print(speed)
            if event.key == pygame.K_DOWN:
                speed = speed-inc
                if speed <= 0:
                    speed = inc
                print(speed)
            if event.key == pygame.K_SPACE:
                play = (play==False)
            if event.key == pygame.K_BACKSPACE:
                grid = grid_init_blank()
                gridaux = grid_init_blank()
            if event.key == pygame.K_r:
                grid = grid_init_rand()
                gridaux = grid_init_blank()
    if play == True:
        for r in range(numrows):
            for c in range(numcols):
                n = get_neighbors(grid,r,c)
                gridaux[r][c] = step(grid[r][c],n)
        grid = gridaux.copy()
        time.sleep(1.0/speed)


    pos = pygame.mouse.get_pos()
    y = (pos[0]//(margin+width))
    x = (pos[1]//(margin+height))

    screen.fill(black)

    tot = 0
    for row in range(numrows):
        for column in range(numcols):   
            color = white
            if grid[row][column] == 1:
                color = orange                        #Color Change
                tot = tot+1
            pygame.draw.rect(screen, color, 
                [(margin+((width+margin)*column)), 
                (margin+((height+margin)*row)), width, height])

    if tot == 0:
        play = False

    clock.tick(20)


    pygame.display.flip()

pygame.quit()
