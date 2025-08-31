import pygame
from classes.spaceship import Spaceship
from classes.constants import *

class Player(Spaceship):

    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def update(self, dt):
        self.velocity = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(1)
        if keys[pygame.K_s]:
            self.move(-1)
        if keys[pygame.K_SPACE]:
            if self.activate_quad_fire:
                self.quad_fire()
                return
            self.shoot()
        
        super().update(dt)

    def move(self, mod):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity = forward * self.ship_speed * mod
        
    def get_player_position(self):
        return self.position

    def rotate(self, dt):
        self.rotation += SHIP_TURN_SPEED * dt