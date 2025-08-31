import pygame
from classes.spaceship import Spaceship
from classes.constants import *
import random

class Enemy_Ship(Spaceship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity_timer = 2
        self.player_position = pygame.Vector2(0, 0)
        self.shoot_timer = 2

    def draw(self, screen):
        pygame.draw.polygon(screen, "red", self.triangle(), 2)

    def update(self, dt):
        super().update(dt)
        
        if self.velocity_timer <= 0:
            self.change_velocity(dt)
            self.velocity_timer = 2
       
        self.velocity_timer -= dt
        self.adjust_rotation()
        self.shoot_player(dt)



        
    def adjust_rotation(self):
        #the direction our sprite faces by default
        forward = pygame.Vector2(0, 1)
        #direction (x, y) to player
        to_player = self.player_position - self.position
        angle = forward.angle_to(to_player)

        self.rotation = angle

    def change_velocity(self, dt):
        #if less than, positive velocity
        if self.position.x < SCREEN_WIDTH * 0.25:
            x = 1
        elif self.position.x > SCREEN_WIDTH * 0.75:
            x = -1
        else:
            x = random.choice([-1, 1])

        if self.position.y < SCREEN_HEIGHT / 2:
            y = 1
        elif self.position.y > SCREEN_HEIGHT / 2:
            y = -1
        else:
            y = random.choice([-1, 1])
        
        self.velocity.x = x
        self.velocity.y = y 

        self.velocity *= (self.ship_speed)

        
    def set_player_position(self, pos):
        self.player_position = pos

    def shoot_player(self, dt):
        self.shoot_timer -= dt

        if self.shoot_timer < 0:
            self.shoot_timer = 2
            self.shoot()

   

    #when spawned sprite face down (0, 1)

    #forward = Vector2(0, 1)
    #to_player = player_pos - enemy_pos
    #angle = forward.angle_to(to_player)