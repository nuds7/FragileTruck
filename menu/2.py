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
screenRect = 0,0,screenWidth,screenHeight
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

mainMenuImg = pygame.image.load('assets/images/mainmenu.png')

class centerImg:
    def __init__(self, image, offsetX, offsetY):
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.image = image
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        screen.blit(image, ((screenWidth/2) - (self.image_width/2) + self.offsetX,(screenHeight/2) - (self.image_height/2 + self.offsetY)))

imgCentered = centerImg(mainMenuImg, 0,0) # Image, offset in x, offset in Y

honk = 0
# Running Loop
while running == True:
    # Input
    key = pygame.key.get_pressed() #Get keys pressed
    if key[pygame.K_RIGHT]:
        pass
    if key[pygame.K_LEFT]:
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
    centerImg(mainMenuImg, 0,0)
    #######################
    pygame.display.update()
    clock.tick(fps_limit)
    #######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
pygame.quit()
