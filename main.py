import pygame
from classes.constants import *
from asteroid_main import Asteroid_Main
from spaceship_main import Spaceship_Main


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    controllers = pygame.sprite.Group()

    Spaceship_Main.containers = (controllers)
    Asteroid_Main.containers = (controllers)
    

    spaceship_main = Spaceship_Main()
    asteroid_main = Asteroid_Main()
  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        controllers.update(dt)

        pygame.Surface.fill(screen, (0,0,0))
        
        for obj in controllers:
            obj.draw(screen)

        #retrieve collidables
        asteroid_collidables = asteroid_main.get_collidables()
        spaceship_collidables = spaceship_main.get_collidables()

        #check for objects colliding and return collisions list
        a_collisions = asteroid_main.check_collision_against(spaceship_collidables)
        s_collisions = spaceship_main.check_collision_against(asteroid_collidables)

        #handle collisions
        asteroid_main.handle_collisions(a_collisions)
        spaceship_main.handle_collisions(s_collisions)

        if not spaceship_main.player_alive():
            print("Game Over")
            return

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
