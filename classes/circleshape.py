import pygame
from classes.constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

        self.despawn_timer = 5
        self.off_screen = True

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        self.off_screen = self.check_if_off_screen()

        if self.despawn_timer <= 0:
            self.kill()
        if self.off_screen:
            self.despawn_timer -= dt
        else:
            self.off_screen = 5
        
    def collision(self, circle):
        #circle represents another object (asteroid/player?) Gonna add feature where collisions between asteroids will bounce of each other
        return True if pygame.Vector2.distance_to(self.position, circle.position) <= self.radius + circle.radius else False
    
    #handles external
    def collision_handle(self):
        self.kill()

    def check_if_off_screen(self):
        position = self.position

        if position.x < 0 or position.x > SCREEN_WIDTH:
            return True

        if position.y < 0 or position.y > SCREEN_HEIGHT:
            return True

        return False
