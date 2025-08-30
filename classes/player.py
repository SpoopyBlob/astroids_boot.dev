from classes.circleshape import CircleShape
from classes.constants import *
import pygame
from classes.shot import Shot
import random

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0
        
        #updated when player gains powerup
        self.player_shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.player_speed = PLAYER_SPEED
        self.indestructable = False
        self.activate_quad_fire = False
        
        #power ups can stack, duration is 10 seconds, once timer has ended, powerup_enabled = False, timer stops
        self.powerup_enabled = False
        self.powerup_timer = 10
 
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        super().update(dt)

        self.update_shot_timer(dt)

        if self.powerup_enabled == True:
            self.update_powerup_timer(dt)
            


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            if self.activate_quad_fire:
                self.quad_fire()
                return
            self.shoot()

    def update_shot_timer(self, dt):
        self.shot_timer -= dt

    def update_powerup_timer(self, dt):
        self.powerup_timer -= dt
        if self.powerup_timer < 0:
            self.powerup_enabled = False

            #remove powerups
            self.player_shoot_cooldown = PLAYER_SHOOT_COOLDOWN
            self.player_speed = PLAYER_SPEED
            self.indestructable = False
            self.activate_quad_fire = False


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.player_speed * dt
    
    def shoot(self):
        if self.shot_timer > 0:
            return

        self.shot_timer = self.player_shoot_cooldown
        bullet = Shot(self.position[0], self.position[1])
        bullet.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def quad_fire(self):
        if self.shot_timer > 0:
            return
        
        self.shot_timer = self.player_shoot_cooldown
        for n in range(0, 360, 90):
            bullet = Shot(self.position[0], self.position[1])
            bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation + n) * PLAYER_SHOOT_SPEED


    def collision_handle(self):
        if self.indestructable == True:
            return
        self.kill()
 

    def power_up_collision(self):
        powerups = ["speed", "shot_speed", "indestructable", "quad_fire"]
        powerup = random.choice(powerups)
        self.powerup_enabled = True
        print(powerup)


        if powerup == "shot_speed":
            self.player_shoot_cooldown *= 0.2
        elif powerup == "speed":
            self.player_speed *= 2
        elif powerup == "indestructable":
            self.indestructable = True
        elif powerup == "quad_fire":
            self.activate_quad_fire = True


    