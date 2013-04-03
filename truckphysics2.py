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

body_space = pymunk.Space()
body_space.gravity = (0,800)


class Car:
    def __init__(self, body_mass, body_position, body_size, wheel_base):
        self.body_mass = body_mass
        self.body_position = body_position
        self.body_size = body_size
        self.body_body = pymunk.Body(self.body_mass, 100)
        self.body_body.position = self.body_position
        self.body_poly = pymunk.Poly.create_box(self.body_body, self.body_size)
        
        self.body_poly.friction = 0.5

        body_space.add(self.body_body, self.body_poly)

        self.wheel_base = wheel_base

        self.wheelL_mass = 1
        self.wheelL_radius = (self.body_size[1]//1.5)
        self.wheelL_position_x = self.body_position[0]-(self.body_size[0]//2)+self.wheelL_radius - self.wheel_base
        self.wheelL_position_y = self.body_position[1] + self.body_size[1] + 20
        self.wheelL_position = self.wheelL_position_x, self.wheelL_position_y
        
        self.inertiaL = pymunk.moment_for_circle(self.wheelL_mass, 0, self.wheelL_radius)
        self.wheelL_b = pymunk.Body(self.wheelL_mass, self.inertiaL)
        self.wheelL_b.position = self.wheelL_position
        self.wheelL_shape = pymunk.Circle(self.wheelL_b, self.wheelL_radius)
        
        self.wheelL_shape.friction = 0.8
        
        space.add(self.wheelL_b, self.wheelL_shape)

        self.wheelR_mass = 1
        self.wheelR_radius = (self.body_size[1]//1.5)
        self.wheelR_position_x = self.body_position[0]+(self.body_size[0]//2)-self.wheelL_radius + self.wheel_base
        self.wheelR_position_y = self.body_position[1] + self.body_size[1] + 20
        self.wheelR_position = self.wheelR_position_x, self.wheelR_position_y
        
        self.inertiaR = pymunk.moment_for_circle(self.wheelR_mass, 0, self.wheelR_radius)
        self.wheelR_b = pymunk.Body(self.wheelR_mass, self.inertiaR)
        self.wheelR_b.position = self.wheelR_position
        self.wheelR_shape = pymunk.Circle(self.wheelR_b, self.wheelR_radius)

        self.wheelR_shape.friction = 0.8
        
        space.add(self.wheelR_b, self.wheelR_shape)

        self.left_spring = pymunk.constraint.DampedSpring(self.body_body, self.wheelL_b, (-self.body_size[0]//2, 0), (0,0), self.wheelL_position_y, 13.0, 2)
        self.right_spring = pymunk.constraint.DampedSpring(self.body_body, self.wheelR_b, (self.body_size[0]//2, 0), (0,0), self.wheelR_position_y, 13.0, 2)
        self.middle_spring = pymunk.constraint.DampedSpring(self.wheelL_b, self.wheelR_b, (0,0), (0,0), self.body_size[0], self.body_size[0], 4)

        self.left_pinjoint = pymunk.constraint.PinJoint(self.body_body, self.wheelL_b, (0,0), (0,0))
        self.right_pinjoint = pymunk.constraint.PinJoint(self.body_body, self.wheelR_b, (0,0), (0,0))

        
        
        space.add(self.left_spring, self.right_spring, self.left_pinjoint, self.right_pinjoint, self.middle_spring)

        #self.wheelL_b.angular_velocity = 0
        #self.wheelR_b.angular_velocity = 0


    def force(self, body_to_impulse, impulse):
        self.impulse = Vec2d(impulse)
        self.body_to_impulse = body_to_impulse
        self.body_to_impulse.apply_impulse(self.impulse)


    def Draw(self, color):
        self.color = color
        
        self.body_rect = self.body_poly.get_points()
        pygame.draw.lines(screen, black, True, self.body_rect, 1)

        self.wheelL_pos = int(self.wheelL_b.position[0]), int(self.wheelL_b.position[1])
        pygame.draw.circle(screen, blue, self.wheelL_pos, int(self.wheelL_radius), 1)


        self.wheelR_pos = int(self.wheelR_b.position[0]), int(self.wheelR_b.position[1])
        pygame.draw.circle(screen, blue, self.wheelR_pos, int(self.wheelR_radius), 1)

        # drawing lines for the spring
        self.p_on_body_body_L_X = self.body_body.position[0] + (-self.body_size[0]//2+self.wheelL_radius)*math.cos(self.body_body.angle)
        self.p_on_body_body_L_Y = self.body_body.position[1] + (-self.body_size[0]//2+self.wheelL_radius)*math.sin(self.body_body.angle)
        self.p_on_body_body_R_X = self.body_body.position[0] + (self.body_size[0]//2-self.wheelL_radius)*math.cos(self.body_body.angle)
        self.p_on_body_body_R_Y = self.body_body.position[1] + (self.body_size[0]//2-self.wheelL_radius)*math.sin(self.body_body.angle) 
        
        self.spring_line_left = self.p_on_body_body_L_X, self.p_on_body_body_L_Y
        self.spring_line_right = self.p_on_body_body_R_X, self.p_on_body_body_R_Y

        
        self.spring_lines = self.spring_line_left, self.wheelL_b.position, self.wheelR_b.position, self.spring_line_right
        pygame.draw.lines(screen, self.color, False, self.spring_lines, 1)

        # drawing lines on wheels
        self.p_on_wheel_body_L_X = self.wheelL_pos[0] + (self.wheelL_radius)*math.cos(self.wheelL_b.angle)
        self.p_on_wheel_body_L_Y = self.wheelL_pos[1] + (self.wheelL_radius)*math.sin(self.wheelL_b.angle)

        pygame.draw.line(screen, blue, (self.wheelL_pos), (self.p_on_wheel_body_L_X,self.p_on_wheel_body_L_Y), 1)

        self.p_on_wheel_body_R_X = self.wheelR_pos[0] + (self.wheelR_radius)*math.cos(self.wheelR_b.angle)
        self.p_on_wheel_body_R_Y = self.wheelR_pos[1] + (self.wheelR_radius)*math.sin(self.wheelR_b.angle)

        pygame.draw.line(screen, blue, (self.wheelR_pos), (self.p_on_wheel_body_R_X,self.p_on_wheel_body_R_Y), 1)
        
        
car_Body = Car(1, (100, 100), (100,20), 0)

crateImg = pygame.image.load('assets/images/crate.png')

class boxes:
    def __init__(self, position, mass, size, friction):
        self.position = position
        self.mass = mass
        self.size = size
        self.friction = friction
        self.box_body = pymunk.Body(self.mass, 20)
        self.box_body.position = self.position
        self.box_shape = pymunk.Poly.create_box(self.box_body, self.size)
        self.box_shape.friction = self.friction

        space.add(self.box_body, self.box_shape)

    def draw(self, color):
        self.color = color
        self.box_rect = self.box_shape.get_points()

        pygame.draw.lines(screen, self.color, True, self.box_rect, 1)

crates = boxes((300,300), .2, (10,10), .8)

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

static_Floor = static_shapes((screenWidth - 10, 10), ((screenWidth/2), screenHeight-20), 1)


# Running Loop
while running == True:
    # Input
    key = pygame.key.get_pressed() #Get keys pressed
    if key[pygame.K_UP]:
        car_Body.force(car_Body.body_body,(0,-60))
    if key[pygame.K_LEFT]:
        car_Body.wheelL_b.angular_velocity -= 6
    if key[pygame.K_RIGHT]:
        car_Body.wheelL_b.angular_velocity += 6
    mousePos = pygame.mouse.get_pos() #Get mouse position
    clicks = pygame.mouse.get_pressed()
    if clicks == (1,0,0):
        pass
    
    # End Input
    # Logic
    
    ##Physics
    space.step(0.02)
    body_space.step(0.02)
    car_Body.wheelL_b.angular_velocity *= .8
    ##
    # Drawing
    screen.fill(white)
    car_Body.Draw(red)
    static_Floor.Draw(black)
    crates.draw(black)
    #######################
    pygame.display.update()
    clock.tick(fps_limit)
    #######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
pygame.quit()
