import pygame, math, random
from random import uniform, randrange
from pygame.locals import * # allows me to use "K_UP", etc.
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
space.gravity = (0,800)

class Car:
    def __init__(self, body_mass, body_position, body_size):
        self.body_mass = body_mass
        self.body_position = body_position
        self.body_size = body_size
        self.body_body = pymunk.Body(self.body_mass, 1000)
        self.body_body.position = self.body_position
        self.body_poly = pymunk.Poly.create_box(self.body_body, self.body_size)

        space.add(self.body_body, self.body_poly)

        self.wheelL_mass = 1
        self.wheelL_radius = (self.body_size[1]//1.5)
        self.wheelL_position = self.body_position[0]-(self.body_size[0]//2)+self.wheelL_radius, self.body_position[1] + self.body_size[1]*1.5
        
        self.inertiaL = pymunk.moment_for_circle(self.wheelL_mass, 0, self.wheelL_radius)
        self.wheelL_b = pymunk.Body(self.wheelL_mass, self.inertiaL)
        self.wheelL_b.position = self.wheelL_position
        self.wheelL_shape = pymunk.Circle(self.wheelL_b, self.wheelL_radius)
        
        space.add(self.wheelL_b, self.wheelL_shape)

        self.wheelR_mass = 1
        self.wheelR_radius = (self.body_size[1]//1.5)
        
        self.wheelR_position = self.body_position[0]+(self.body_size[0]//2)-self.wheelL_radius, self.body_position[1] + self.body_size[1]*1.5
        
        self.inertiaR = pymunk.moment_for_circle(self.wheelR_mass, 0, self.wheelR_radius)
        self.wheelR_b = pymunk.Body(self.wheelR_mass, self.inertiaR)
        self.wheelR_b.position = self.wheelR_position
        self.wheelR_shape = pymunk.Circle(self.wheelR_b, self.wheelR_radius)
        
        space.add(self.wheelR_b, self.wheelR_shape)

    def Draw(self, color):
        self.color = color
        
        self.body_rect = self.body_poly.get_points()
        pygame.draw.lines(screen, self.color, True, self.body_rect, 1)

        self.wheelL_pos = int(self.wheelL_b.position[0]), int(self.wheelL_b.position[1])
        pygame.draw.circle(screen, self.color, self.wheelL_pos, int(self.wheelL_radius), 1)

        self.wheelR_pos = int(self.wheelR_b.position[0]), int(self.wheelR_b.position[1])
        pygame.draw.circle(screen, self.color, self.wheelR_pos, int(self.wheelR_radius), 1)

car_Body = Car(1, (100, 100), (100,20))

class static_shapes:
    def __init__(self, size, position, friction):
        self.size = size
        self.position = position
        self.friction = friction
        
        self.body = pymunk.Body()  # statics are created by not passing args through body constructor
        self.body.position = self.position
        self.static_box = pymunk.Poly.create_box(self.body, self.size)
        self.static_box.friction = self.friction

        space.add(self.static_box)

    def Draw(self, color):
        self.color = color
        self.rect = self.static_box.get_points()
        pygame.draw.lines(screen, self.color, True, self.rect, 1)

static_Floor = static_shapes((screenWidth - 10, 10), ((screenWidth/2), screenHeight-20), .4)

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
    car_Body.Draw(red)
    static_Floor.Draw(black)

    #######################
    pygame.display.update()
    clock.tick(fps_limit)
    #######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
pygame.quit()
