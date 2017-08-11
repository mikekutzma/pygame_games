#This is the game of life

import pygame
import random
import time
import numpy as np
import math
import sys
import runlengthencoded as rle

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

height = 5
width = 5
margin = 1

iso = 1
ovrc = 4
gen = 3

speed = 5.0
inc = 1.0

numrows = 90
numcols = 90

margincolor = black
deadcellcolor = pink
livecellcolor = blue

textcolor = white

gosperfile = 'gosperglidergun.rle'

sizevert = margin + ((margin + height) * numrows)
sizehorz = margin + ((margin + width) * numcols)

size = [sizehorz, sizevert]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("The Game of Life")

clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial Bold',25)

if(len(sys.argv)>1):
    logging = True
    filename = sys.argv[1]
else:
    logging=False

if(logging):
    f = open(filename,'w')

def grid_init_blank():
    grid = np.zeros((numrows,numcols))
    return grid

def grid_init_rand():
    grid = np.floor(np.random.random((numrows,numcols))*2).astype(int)
    return grid

def get_neighbors(grid,x,y):
    total = 0
    for i in range(-1,2):
        for j in range(-1,2):
            total+=grid[(x+i)%numrows][(y+j)%numcols]
    total = total - grid[x][y]
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

def get_num_cells(g):
    dead = len(list(filter(lambda x: x==0,g.flatten())))
    live = len(list(filter(lambda x: x==1,g.flatten())))
    return [dead,live]

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_UP:
                speed = speed+inc
            if event.key == pygame.K_DOWN:
                speed = speed-inc
                if speed <= 0:
                    speed = inc
            if event.key == pygame.K_SPACE:
                play = (play==False)
            if event.key == pygame.K_BACKSPACE:
                grid = grid_init_blank()
                gridaux = grid_init_blank()
            if event.key == pygame.K_r:
                grid = grid_init_rand()
                gridaux = grid_init_blank()
            if event.key == pygame.K_g:
                gos_grid = rle.read_rle(gosperfile)
                for i in range(len(gos_grid)):
                    for j in range(len(gos_grid[0])):
                        grid[x+i][y+j] = gos_grid[i][j]
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

    screen.fill(margincolor)

    tot = 0
    for row in range(numrows):
        for column in range(numcols):   
            color = deadcellcolor
            if grid[row][column] == 1:
                color = livecellcolor
                tot = tot+1
            pygame.draw.rect(screen, color, 
                [(margin+((width+margin)*column)), 
                (margin+((height+margin)*row)), width, height])

    deadcells, livecells = get_num_cells(grid)
    if (logging and play): f.write(str(livecells)+"\n")
    deadtext = font.render("Dead: "+str(deadcells), 1, textcolor)
    livetext = font.render("Live: "+str(livecells), 1, textcolor)
    screen.blit(deadtext, (1,1))
    screen.blit(livetext, (100,1))

    if tot == 0:
        play = False

    clock.tick(20)


    pygame.display.flip()

if(logging):
    f.close()

pygame.quit()
