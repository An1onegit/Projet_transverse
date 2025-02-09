import pygame
from library.utils import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Bear's Fishing Empire")

# Load map and add scale it
tile_map = TileMap("sources/maps/mapTest2.tmx")
map_surface = pygame.transform.scale_by(tile_map.surface, tile_map.zoom)

sprite_group = CameraGroup(map_surface)

tile_map.render_objects(sprite_group)

# Create player object
player = Player(pos = (3500, 3500), groups = sprite_group, hitboxes = tile_map.hitboxes)

# Setup clock for delta time and fps limit
fps = 120
clock = pygame.time.Clock()

running = True
while running:
    # Calculate delta time (time since last frame)
    dt = clock.tick(fps) / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        else:
            player.anim = 5

    # Clear the screen
    screen.fill((134, 203, 146))

    sprite_group.update(dt)
    sprite_group.custom_draw(player)

    # update the display
    pygame.display.flip()

pygame.quit()