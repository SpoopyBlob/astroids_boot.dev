import pygame
from classes.asteroid import Asteroid
from classes.constants import *

class Transforming_Asteroid(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, TRANSFORMING_ASTEROID_RADIUS)
        #once health reaches 0, asteroid will transform
        self.health = 10
        self.collisions_till_transformation = 8
        
    def update(self, dt):
        super().update(dt)
        
        if self.health <= 0:
            self.kill()

            
    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def collision_handle(self):
        if self.check_if_off_screen() == False:

            self.collisions_till_transformation -= 1
            self.radius += 5

    def external_collision(self):
        self.health -= 1

    def __add__(self, obj):
        self.health += obj.health
        self.radius += 20
        if self.radius < 160:
            self.collisions_till_transformation = 0

        obj.kill()

    