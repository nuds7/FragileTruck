import pygame, math, random
from random import uniform, randrange
from pygame.locals import * # allows me to use "K_UP", etc.
# from vec2d import *
import pymunk
from pymunk import Vec2d
pygame.init()
# Settings
screenWidth = 900
screenHeight = 600
screenRes = screenWidth,screenHeight
clock = pygame.time.Clock()
running = True
fps_limit = 60
font = pygame.font.Font(None, 12)
screen = pygame.display.set_mode(screenRes)
# Colors
red     = 255,0,0
green   = 0,255,0
blue    = 0,0,255
black   = 0,0,0
white   = 255,255,255
#####################
space = pymunk.Space()
space.gravity = (0,900)


# Running Loop
while running == True:
    # Input
    key = pygame.key.get_pressed() #Get keys pressed
    if key[pygame.K_UP]:
        pass
    mousePos = pygame.mouse.get_pos() #Get mouse position
    clicks = pygame.mouse.get_pressed()
    if clicks == (1,0,0):
        pass
    
    # End Input
    # Logic
    
    ##Physics
    space.step(0.02)
    ##
    # Drawing
    screen.fill(white)

    #######################
    pygame.display.update()
    clock.tick(fps_limit)
    #######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
pygame.quit()
