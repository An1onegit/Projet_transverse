import pygame
import math
from pytmx.util_pygame import load_pygame
from library.menu import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)



def Main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Bear's Fishing Empire")

    clock = pygame.time.Clock()
    running = True

    fps = 120
    clock = pygame.time.Clock()

    tmx_data = load_pygame('sources/maps/mapTest2.tmx')
    sprite_group = pygame.sprite.Group()

    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x*32, y*32)
                Tile(pos= pos, surf= surf, groups=sprite_group)

    # Player's caracteristics
    ## Coordinates 
    x = 250
    y = 250

    ##Size
    width = 50
    height = 50

    # Speed
    speed = 800

    while running:
        # Calculate delta time (time since last frame)
        dt = clock.tick(fps) / 1000.0  # Convert milliseconds to seconds

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((134, 203, 146) )

        # Player's movements
        keys = pygame.key.get_pressed()
        
        # Initialize movement variables
        x_change = 0
        y_change = 0

        # Handle key inputs
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x_change += 1   
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            x_change -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y_change += 1
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            y_change -= 1

        # Normalize diagonal movement
        if x_change != 0 and y_change != 0:
            # Divide each component by sqrt(2) to normalize the vector
            x_change /= math.sqrt(2)
            y_change /= math.sqrt(2)

        # Update the position
        x += x_change * speed * dt
        y += y_change * speed * dt

        # RENDER YOUR GAME HERE
        sprite_group.draw(screen)

        pygame.draw.rect(screen,(57, 42, 22),(x,y,width,height))

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(fps)  # limits FPS to 60

    pygame.quit()

    
if MainMenu():
    Main()