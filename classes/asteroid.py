from classes.circleshape import CircleShape
from classes.constants import *
import pygame
import random

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        #timer for collision_exception once collision has happend
        self.collision_exception = 2

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        super().update(dt)
        
        #self.position += self.velocity * dt
        #timer for collision_exception
        if self.collision_exception > 0: 
            self.collision_exception -= dt

        
    def collision_handle(self):
        super().collision_handle()

        #if object is at a minimum radius, no split occurs, object gets removed
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

        #if both objects are transforming_asteroids, combine
        if obj.__class__.__name__ == "Transforming_Asteroid":
            if self.__class__.__name__ == "Transforming_Asteroid":
                self = self + obj
                return
            
        #if objects are equal in size, they bounce of each other
        if self.radius == obj.radius:
            self.angle_to_event(obj)
            obj.angle_to_event(self)

            self.collision_exception = 0.5
            obj.collision_exception = 0.5

        #if one object is bigger then another, the smaller one splits (see collision_handle)
        elif self.radius < obj.radius:
            self.collision_handle()
            obj.collision_exception = 0.5
            #if transforming_asteroid, perform collision handle (updates collisions_till_transformation var)
            if obj.__class__.__name__ == "Transforming_Asteroid":
                obj.collision_handle()
                
        else:
            obj.collision_handle()
            self.collision_exception = 0.5
            if self.__class__.__name__ == "Transforming_Asteroid":
                self.collision_handle()


    def angle_to_event(self, obj):
        forward = pygame.Vector2(0, 1)
        face_away = self.position - obj.position
        angle = forward.angle_to(face_away)
        self.rotation = angle
        self.velocity = face_away.normalize() * 100
        

                

    