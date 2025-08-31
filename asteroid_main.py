from classes.asteroid import Asteroid
from classes.asteroidField import AsteroidField
from classes.transforming_asteroid import Transforming_Asteroid
import pygame

class Asteroid_Main(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.asteroid_to_transform = []
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
                for i in obj:
                    #checks collision status of transforming_asteroid after internal collision
                    if i.__class__.__name__ == "Transforming_Asteroid":
                        self.check_transformation_status(i)

            #else we are handling external collisions
            else:
                #edge case: transforming_asteroids lose health
                if obj.__class__.__name__ == "Transforming_Asteroid":
                    obj.external_collision()
                else:
                    obj.collision_handle()

    #checks if a transforming asteroid is ready to transform
    def check_transformation_status(self, obj):
        if obj.collisions_till_transformation <= 0:
            self.asteroid_to_transform.append(obj.position)
            obj.kill()
            self.transformation_event(obj)

    #getter method for main to transfer information between asteroid_main and spaceship_main
    def get_asteroid_to_transform(self):
        return_asteroids = self.asteroid_to_transform.copy()
        self.asteroid_to_transform = []
        return return_asteroids

    def transformation_event(self, event_obj):
        for asteroid in self.a_draw:
            asteroid.angle_to_event(event_obj)
        





    