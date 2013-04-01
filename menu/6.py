import pygame, math, random
from random import uniform, randrange
from pygame.locals import *  # allows me to use "K_UP", etc.
# from vec2d import *
import pymunk
from pymunk import Vec2d
import time
print("All assets loaded successfully")
pygame.init()
# Settings
screenWidth = 900
screenHeight = 600
screenRes = screenWidth, screenHeight
clock = pygame.time.Clock()
running = True
fps_limit = 60
font = pygame.font.Font(None, 12)
screen = pygame.display.set_mode(screenRes)
# Colors
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
black = 0, 0, 0
white = 255, 255, 255
#####################
space = pymunk.Space()
space.gravity = (0, 900)

menuLogoImg = pygame.image.load('assets/images/logo.png')
mainMenuImg = pygame.image.load('assets/images/mainmenucomp.png')
mainMenuBGGlow = pygame.image.load('assets/images/mainmenubackglow.png')
bgImg = pygame.image.load('assets/images/bg.png')
highlightImg = pygame.image.load('assets/images/menuhighlight.png')
highlightImg2 = pygame.image.load('assets/images/menuhighlight2.png')
mainMenuButText = pygame.image.load('assets/images/mainmenubuttontext.png')

class centerImg:
    def __init__(self, image, offset):
        self.offset = offset
        self.image = image
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.offsetX = (screenWidth/2) - (self.image_width/2) - self.offset[0]
        self.offsetY = (screenHeight/2) - (self.image_height/2 - self.offset[1])
        screen.blit(image, (self.offsetX, self.offsetY))
mainMenuImgCentered = centerImg(mainMenuImg, (0,0)) # Image, offset in x, offset in Y
bgImgCentered = centerImg(bgImg, (0,0))
logoImgCentered = centerImg(menuLogoImg, (0,0))
mainMenuButTextCentered = centerImg(mainMenuButText, (0,0))

buttonActivate = False
buttonNum = 0
centerImg(bgImg, (0, 0))  # background img
class menuHighlights:
    def __init__(self, hlImg, hlOffset):
        global buttonActivate
        global buttonNum
        buttonActivate = False
        for i in range(4):  # number of buttons
            self.hlOffset = hlOffset
            # iterating over the range and adding 61px (the height of the buttons)
            self.hlOffset[1] += 61
            self.hlImg = hlImg
            self.hlImg_width = self.hlImg.get_width()
            self.hlImg_height = self.hlImg.get_height()
            ## centering the image
            self.centerX = (screenWidth/2) - (self.hlImg_width/2) - self.hlOffset[0]
            # adding 11px to align with the buttons
            self.centerY = (screenHeight/2) - (self.hlImg_height/2 - self.hlOffset[1]) + 11
            ##
            # setting a 1x1 rect at the mouse pos
            # detecting if the img rect contains the mouse rect
            # sets draw bool == True, draws the highlight
            # will definitelty be adapted for clickables
            self.mousePos = pygame.mouse.get_pos()
            self.mouseRect = (self.mousePos, (1, 1))
            self.highlightRectO = highlightImg.get_rect()
            self.highlightRectO[0] = self.centerX
            self.highlightRectO[1] = self.centerY
            self.highlightRect = self.highlightRectO
            if self.highlightRect.contains(self.mouseRect):
                screen.blit(hlImg, (self.centerX, self.centerY))
                buttonActivate = True
                buttonNum = i + 1  # adding 1 so that the first button == 1
            if self.highlightRect.contains(self.mouseRect):
                screen.blit(mainMenuBGGlow, (self.centerX - 38, self.centerY-34))

menuHighlight = menuHighlights(highlightImg, [0, 0])

clicked = False
# Running Loop
mousePos2 = 0,0
while running == True:
    pygame.display.set_caption(str(int(clock.get_fps())))
    # Input
    key = pygame.key.get_pressed()  # Get keys pressed
    if key[pygame.K_RIGHT]:
        pass
    if key[pygame.K_LEFT]:
        pass
    mousePos1 = pygame.mouse.get_pos()  # Get mouse position
    clicks = pygame.mouse.get_pressed()
    if clicks == (1, 0, 0) and buttonNum == 1:  # play
        highlightImg = highlightImg2
        clicked = True
    elif clicks == (1, 0, 0) and buttonNum == 2:  # highscores
        highlightImg = highlightImg2
        clicked = True
    elif clicks == (1, 0, 0) and buttonNum == 3:  # instructions
        highlightImg = highlightImg2
        clicked = True
    elif clicks == (1, 0, 0) and buttonNum == 4:  # exit
        highlightImg = highlightImg2
        clicked = True
    else:
        highlightImg = pygame.image.load('assets/images/menuhighlight.png')
        clicked = False
    # End Input
    # Logic
    if buttonActivate:
        print("Button number: " + str(buttonNum), str(clicked))
    ##Physics
    space.step(0.02)
    ##
    # Drawing
    
    centerImg(bgImg, (0, 0))  # background img
    centerImg(mainMenuImg, (0, 0))  # main menu img
    # centerImg(menuLogoImg, (0, -130))
    menuHighlights(highlightImg, [0, -61])
    centerImg(mainMenuButText, (0, 104))
    
    
    #######################
    pygame.display.update()
    clock.tick(fps_limit)
    #######################
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
pygame.quit()
