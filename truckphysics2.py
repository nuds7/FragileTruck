import pygame, math, random
from random import uniform, randrange
from pygame.locals import * # allows me to use "K_UP", etc.
import pymunk
from pymunk import Vec2d
pygame.init()
# Settings
screenWidth = 1000
screenHeight = 700
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
        self.body_body = pymunk.Body(self.body_mass, 200)
        self.body_body.position = self.body_position
        self.body_poly = pymunk.Poly.create_box(self.body_body, self.body_size)
        
        self.body_poly.friction = 0.5

        body_space.add(self.body_body, self.body_poly)

        self.wheel_base = wheel_base

        self.wheelL_mass = 1
        self.wheelL_radius = (self.body_size[1]//1.5)
        self.wheelL_position_x = self.body_position[0]-(self.body_size[0]//2)+self.wheelL_radius - self.wheel_base
        self.wheelL_position_y = self.body_position[1] + self.body_size[1]
        self.wheelL_position = self.wheelL_position_x, self.wheelL_position_y
        
        self.inertiaL = pymunk.moment_for_circle(self.wheelL_mass, 0, self.wheelL_radius)
        self.wheelL_b = pymunk.Body(self.wheelL_mass, 100)
        self.wheelL_b.position = self.wheelL_position
        self.wheelL_shape = pymunk.Circle(self.wheelL_b, self.wheelL_radius)
        
        self.wheelL_shape.friction = 0.8
        
        space.add(self.wheelL_b, self.wheelL_shape)

        self.wheelR_mass = 1
        self.wheelR_radius = (self.body_size[1]//1.5)
        self.wheelR_position_x = self.body_position[0]+(self.body_size[0]//2)-self.wheelL_radius + self.wheel_base
        self.wheelR_position_y = self.body_position[1] + self.body_size[1]
        self.wheelR_position = self.wheelR_position_x, self.wheelR_position_y
        
        self.inertiaR = pymunk.moment_for_circle(self.wheelR_mass, 0, self.wheelR_radius)
        self.wheelR_b = pymunk.Body(self.wheelR_mass, 100)
        self.wheelR_b.position = self.wheelR_position
        self.wheelR_shape = pymunk.Circle(self.wheelR_b, self.wheelR_radius)

        self.wheelR_shape.friction = 0.8
        
        space.add(self.wheelR_b, self.wheelR_shape)

        self.rest_ln = 40
        self.stiff = 80.0
        self.damp = 14
        self.left_spring1 = pymunk.constraint.DampedSpring(self.body_body, self.wheelL_b, (-self.body_size[0]//2 + self.wheelL_radius*2, 0), (0,0), self.rest_ln, self.stiff, self.damp)
        self.left_spring2 = pymunk.constraint.DampedSpring(self.body_body, self.wheelL_b, (-self.body_size[0]//2 - self.wheelL_radius*2, 0), (0,0), self.rest_ln, self.stiff, self.damp)

        self.right_spring1 = pymunk.constraint.DampedSpring(self.body_body, self.wheelR_b, (self.body_size[0]//2 + self.wheelL_radius*2, 0), (0,0), self.rest_ln, self.stiff, self.damp)
        self.right_spring2 = pymunk.constraint.DampedSpring(self.body_body, self.wheelR_b, (self.body_size[0]//2 - self.wheelL_radius*2, 0), (0,0), self.rest_ln, self.stiff, self.damp)
        self.middle_spring = pymunk.constraint.DampedSpring(self.wheelL_b, self.wheelR_b, (0,0), (0,0), self.body_size[0]+self.wheel_base, self.stiff, 8)

        space.add(self.left_spring1, self.left_spring2, self.right_spring1, self.right_spring2, self.middle_spring)


    def force(self, body_to_impulse, impulse):
        self.impulse = Vec2d(impulse)
        self.body_to_impulse = body_to_impulse
        self.body_to_impulse.apply_impulse(self.impulse)


    def Draw(self, color):
        self.color = color
        
        self.body_rect = self.body_poly.get_points()
        pygame.draw.lines(screen, self.color, True, self.body_rect, 1)

        self.wheelL_pos = int(self.wheelL_b.position[0]), int(self.wheelL_b.position[1])
        pygame.draw.circle(screen, self.color, self.wheelL_pos, int(self.wheelL_radius), 1)

        self.wheelR_pos = int(self.wheelR_b.position[0]), int(self.wheelR_b.position[1])
        pygame.draw.circle(screen, self.color, self.wheelR_pos, int(self.wheelR_radius), 1)

        # drawing lines for the spring
        self.p_on_body_body_L_X = self.body_body.position[0] + (-self.body_size[0]//2+self.wheelL_radius)*math.cos(self.body_body.angle)
        self.p_on_body_body_L_Y = self.body_body.position[1] + (-self.body_size[0]//2+self.wheelL_radius)*math.sin(self.body_body.angle)
        self.p_on_body_body_R_X = self.body_body.position[0] + (self.body_size[0]//2-self.wheelL_radius)*math.cos(self.body_body.angle)
        self.p_on_body_body_R_Y = self.body_body.position[1] + (self.body_size[0]//2-self.wheelL_radius)*math.sin(self.body_body.angle) 
        self.spring_line_left = self.p_on_body_body_L_X, self.p_on_body_body_L_Y
        self.spring_line_right = self.p_on_body_body_R_X, self.p_on_body_body_R_Y
        self.spring_lines = (self.spring_line_left, self.wheelL_b.position, self.wheelR_b.position, self.spring_line_right)
        pygame.draw.lines(screen, self.color, False, self.spring_lines, 1)

        # drawing lines on wheels
        self.p_on_wheel_body_L_X = self.wheelL_pos[0] + (self.wheelL_radius)*math.cos(self.wheelL_b.angle)
        self.p_on_wheel_body_L_Y = self.wheelL_pos[1] + (self.wheelL_radius)*math.sin(self.wheelL_b.angle)
        pygame.draw.line(screen, red, (self.wheelL_pos), (self.p_on_wheel_body_L_X,self.p_on_wheel_body_L_Y), 1)

        self.p_on_wheel_body_R_X = self.wheelR_pos[0] + (self.wheelR_radius)*math.cos(self.wheelR_b.angle)
        self.p_on_wheel_body_R_Y = self.wheelR_pos[1] + (self.wheelR_radius)*math.sin(self.wheelR_b.angle)
        pygame.draw.line(screen, red, (self.wheelR_pos), (self.p_on_wheel_body_R_X,self.p_on_wheel_body_R_Y), 1)

        
car_Body = Car(1, (100, 100), (70,20), 0)

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

crates = boxes((300,300), .2, (20,20), .8)

# Static rectangles
class static_shapes:
    def __init__(self, size, position, friction, angle):
        self.size = size
        self.position = position
        self.friction = friction
        self.angle = angle
        self.body = pymunk.Body()  # statics are created by not passing args through body constructor
        self.body.position = self.position
        self.static_box = pymunk.Poly.create_box(self.body, self.size)
        self.body.angle = self.angle
        self.static_box.friction = self.friction

        space.add(self.static_box)

    def Draw(self, color):
        self.color = color
        self.rect = self.static_box.get_points()
        pygame.draw.lines(screen, self.color, True, self.rect, 1)

static_Floor = static_shapes((screenWidth - 10, 10), ((screenWidth/2), screenHeight-20), 1, 0)

ramp = static_shapes((200, 10), ((screenWidth/2)-95, screenHeight-42), .8, 160)
ramp2 = static_shapes((200, 10), ((screenWidth/2)+95, screenHeight-42), .8, -160)

# Centering images on a body.
car_body_image = pygame.image.load('assets/images/truck.png')
new_car_body_image = car_body_image.convert_alpha()
crateImg = pygame.image.load('assets/images/crate.png')
newCrateImg = crateImg.convert_alpha()
tireImg = pygame.image.load('assets/images/tire.png')
newTireImg = tireImg.convert_alpha()

class Center_Rotate:
    def __init__(self, original_image):
        self.original_image = original_image # alpha converted image

    def draw(self, position, degrees_to_rotate):
        self.position = position # position of body
        self.degrees_to_rotate = degrees_to_rotate # rotation of body
        self.rotation_angle = (math.degrees(self.degrees_to_rotate))*-1

        self.new_rotated_image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.image_offset = Vec2d(self.new_rotated_image.get_size()) / 2.0
        self.new_image_position = self.position - self.image_offset

        screen.blit(self.new_rotated_image, self.new_image_position)

truck_image_rotate = Center_Rotate(new_car_body_image)
crate_image_rotate = Center_Rotate(newCrateImg)
tire_image_rotate = Center_Rotate(newTireImg)

bgImg = pygame.image.load('assets/images/bg.png')

# Running Loop
while running == True:
    # Input
    key = pygame.key.get_pressed() #Get keys pressed
    if key[pygame.K_UP]:
        car_Body.force(car_Body.body_body,(0,-60))
    if key[pygame.K_DOWN]:
        car_Body.force(car_Body.body_body,(0,10))
    if key[pygame.K_LEFT]:
        car_Body.wheelL_b.angular_velocity -= 5
        car_Body.wheelR_b.angular_velocity -= 1
    if key[pygame.K_RIGHT]:
        car_Body.wheelL_b.angular_velocity += 5
        car_Body.wheelR_b.angular_velocity += 1
    mousePos = pygame.mouse.get_pos() #Get mouse position
    clicks = pygame.mouse.get_pressed()
    if clicks == (1,0,0):
        pass
    
    # End Input
    # Logic
    
    ##Physics
    space.step(0.02)
    body_space.step(0.02)
    car_Body.wheelL_b.angular_velocity *= .88
    #car_Body.wheelR_b.angular_velocity *= .88
    ##
    # Drawing
    #screen.blit(bgImg, (0,0))
    screen.fill(white)
    car_Body.Draw(blue)
    static_Floor.Draw(black)
    # crates.draw(black)
    ramp.Draw(black)
    ramp2.Draw(black)
    crate_image_rotate.draw(crates.box_body.position, crates.box_body.angle)
    truck_image_rotate.draw(car_Body.body_body.position, car_Body.body_body.angle)
    tire_image_rotate.draw(car_Body.wheelL_b.position, car_Body.wheelL_b.angle)
    tire_image_rotate.draw(car_Body.wheelR_b.position, car_Body.wheelR_b.angle)
    #######################
    pygame.display.update()
    clock.tick(fps_limit)
    #######################
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                running = False
pygame.quit()
