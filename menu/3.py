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

menuLogoImg = pygame.image.load('assets/images/logo.png')
mainMenuImg = pygame.image.load('assets/images/mainmenu.png')
bgImg = pygame.image.load('assets/images/bg.png')
highlightImg = pygame.image.load('assets/images/menuhighlight.png')
mainMenuButText = pygame.image.load('assets/images/mainmenubuttontext.png')
class centerImg:
    def __init__(self, image, offset):
        self.offset = offset
        self.image = image
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        screen.blit(image, ((screenWidth/2) - (self.image_width/2) - self.offset[0],(screenHeight/2) - (self.image_height/2 - self.offset[1])))
mainMenuImgCentered = centerImg(mainMenuImg, (0,0)) # Image, offset in x, offset in Y
bgImgCentered = centerImg(bgImg, (0,0))
logoImgCentered = centerImg(menuLogoImg, (0,0))
mainMenuButTextCentered = centerImg(mainMenuButText, (0,0))
class menuHighlights:
    def __init__(self, hlImg, hlOffset):
        self.hlOffset = hlOffset
        self.hlImg = hlImg
        self.hlImg_width = self.hlImg.get_width()
        self.hlImg_height = self.hlImg.get_height()
        screen.blit(hlImg, ((screenWidth/2) - (self.hlImg_width/2) - self.hlOffset[0],(screenHeight/2) - (self.hlImg_height/2 - self.hlOffset[1])+ 11))
menuHighlight = menuHighlights(highlightImg, (0,0))

class MenuMouseRect:
    def __init__(self, mousePosition):
        self.mousePosition = mousePosition
        self.mouseRect = pygame.Rect(self.mousePosition,(1,1))
mouseRect = MenuMouseRect((0,0))

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

    
    MenuMouseRect(mousePos)
    # End Input
    # Logic
    
    
    ##Physics
    space.step(0.02)
    ##
    # Drawing
    screen.fill(white)
    centerImg(bgImg, (0,0)) # background img
    centerImg(mainMenuImg, (0,0))# main menu img
    centerImg(menuLogoImg, (0,-130))
    menuHighlights(highlightImg, (0,0))
    centerImg(mainMenuButText, (0,104))
    
    #######################
    pygame.display.update()
    clock.tick(fps_limit)
    #######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
pygame.quit()
