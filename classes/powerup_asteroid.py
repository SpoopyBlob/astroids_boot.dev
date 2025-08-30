import pygame
from classes.asteroid import Asteroid
from classes.constants import *
import random


class Powerup_Asteroid(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, ASTEROID_MIN_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.position, self.radius, 2)

