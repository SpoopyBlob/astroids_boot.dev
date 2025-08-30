from classes.asteroid import Asteroid
from classes.asteroidField import AsteroidField
import pygame

class Asteroid_Main(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.a_update = pygame.sprite.Group()
        self.a_draw = pygame.sprite.Group()
    
        Asteroid.containers = (self.a_update, self.a_draw)
        AsteroidField.containers = (self.a_update,)

        self.astro_field = AsteroidField()

    def update(self, dt):
        #checks for internal collisions every tick
        collisions = self.check_internal_collisions()
        if not collisions == None:
            self.handle_collisions(collisions)

        self.a_update.update(dt)

    def draw(self, screen):
        for obj in self.a_draw:
            obj.draw(screen)

    def get_collidables(self):
        
        return self.a_draw


    def check_collision_against(self, group):
        collisions = []
        
        for a in self.a_draw:
            for obj in group:
                if a.collision(obj):
                    collisions.append(a)


        return collisions

    def check_internal_collisions(self):
        collision_pairs = []

        for a in self.a_draw:
            for a_2 in self.a_draw:
                if a != a_2:
                    if a.collision(a_2):
                    #stops duplicates due to nested loop
                        if (a_2, a) in collision_pairs:
                            continue

                        collision_pairs.append((a, a_2))

        return collision_pairs
    
    def handle_collisions(self, col_list):

        for obj in col_list:
            #if tuple, meaning we are handling internal collisions
            if type(obj) == tuple:
                obj[0].internal_collision_handle(obj[1])
                continue
            #else we are handling external collisions
            obj.collision_handle()

    