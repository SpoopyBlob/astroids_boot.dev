from classes.circleshape import CircleShape
from classes.constants import *
import pygame
import random

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.collision_exception = 2

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)
        if self.collision_exception > 0: 
            self.collision_exception -= dt

    def collision_handle(self):
        
        super().collision_handle()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x + new_radius, self.position.y + new_radius, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x - new_radius, self.position.y - new_radius, new_radius)
        asteroid.velocity = b * 1.2

    def internal_collision_handle(self, obj):
        #collision exception is used on collision to prevent objects getting stuck

        if self.radius == obj.radius:
            self.velocity *= -1
            obj.velocity *= -1

            self.collision_exception = 0.5
            obj.collision_exception = 0.5

        elif self.radius < obj.radius:
            self.collision_handle()
            obj.collision_exception = 0.5
        else:
            obj.collision_handle()
            self.collision_exception = 0.5

    