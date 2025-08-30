import pygame
from classes.player import Player
from classes.constants import *
from classes.shot import Shot


class Spaceship_Main(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.s_update = pygame.sprite.Group()
        self.s_draw = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

        Player.containers = (self.s_update, self.s_draw, self.players)
        Shot.containers = (self.s_update, self.s_draw)

        self.player_one = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def update(self, dt):
        self.s_update.update(dt)

    def draw(self, screen):
        for obj in self.s_draw:
            obj.draw(screen)

    def get_collidables(self):
        return self.s_draw

    def check_collision_against(self, group):
        collisions = []
        
        for s in self.s_draw:
            for obj in group:
                if s.collision(obj):
                    collisions.append(s)

        return collisions

    def handle_collisions(self, col_list):
        for obj in col_list:
            obj.collision_handle()

    def check_internal_collisions(self):
        for s in self.s_draw:
            for s_2 in self.s_draw:
                if s.collision(s_2):
                    s.collision_handle()


        