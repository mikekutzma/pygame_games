#This is the game of life

import pygame
import random
import time

black = 	[0, 0, 0	]
white = 	[255, 255, 255	]
green  = 	[0, 255, 0  	]
red = 		[255, 0, 0      ]
blue = 		[0, 0, 255     	]
yellow = 	[255, 255, 0	]
pink = 		[255, 0, 127	]
orange = 	[255, 128, 0	]
purple = 	[102, 0, 204	]


pygame.init()

height = 10
width = 10
margin = 1

iso = 1
ovrc = 4
gen = 3

speed = 5.0
inc = 1.0

numrows = 60
numcols = 100

sizevert = margin + ((margin + height) * numrows)
sizehorz = margin + ((margin + width) * numcols)

size = [sizehorz, sizevert]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("The Game of Life")

clock = pygame.time.Clock()

grid = []
for row in range(numrows):
	grid.append([])
	for column in range(numcols):
		grid[row].append(0)
gridaux = []
for row in range(numrows):
	gridaux.append([])
	for column in range(numcols):
		gridaux[row].append(0)


done = False
play = False

while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid[x][y] +=1
            if grid[x][y] == 2:
                grid[x][y] = 0
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
                for row in range(numrows):
                    for column in range(numcols):
                        grid[row][column] = 0
    if play == True:
        for row in range(numrows):
            for column in range(numcols):
                sum = 0
                if row > 0:
                    if column > 0:
                        if grid[row-1][column-1] == 1:
                            sum = sum+1
                    if column < numcols-1:
                        if grid[row-1][column+1] == 1:
                            sum = sum+1
                    if grid[row-1][column] == 1:
                        sum = sum+1
                if row < numrows-1:
                    if column > 0:
                        if grid[row+1][column-1] == 1:
                            sum = sum+1
                    if column < numcols-1:
                        if grid[row+1][column+1] == 1:
                            sum = sum+1
                    if grid[row+1][column] == 1:
                        sum = sum+1
                if column > 0:
                    if grid[row][column-1] == 1:
                        sum = sum+1
                if column < numcols-1:
                    if grid[row][column+1] == 1:
                        sum = sum+1
                if grid[row][column] == 1:
                    if sum <= iso or sum >= ovrc:
                        gridaux[row][column] = 0
                    elif sum > iso and sum < ovrc:
                        gridaux[row][column] = 1
                if grid[row][column] == 0:
                    if sum != gen:
                        gridaux[row][column] = 0
                    elif sum == gen:
                        gridaux[row][column] = 1
        for row in range(numrows):
            for column in range(numcols):
                grid[row][column] = gridaux[row][column]
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
