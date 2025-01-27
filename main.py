import pygame
import random
from pytmx.util_pygame import load_pygame

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("sources/img/rpgChar.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("sources/img/rpgChar.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 300  # Movement speed in pixels per second

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        # Handle key inputs
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.direction.x = -1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        elif keys[pygame.K_z] or keys[pygame.K_UP]:
            self.direction.y = -1

    def update(self, dt):
        self.input()
        # Normalize diagonal movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        # Update position
        self.position += self.direction * self.speed * dt
        self.rect.center = self.position

class CameraGroup(pygame.sprite.Group):
    def __init__(self, surf):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.ground_surf = surf
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

    def custom_draw(self):
        self.display_surface.blit(self.ground_surf, self.ground_rect)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect)

class TileMap:
    def __init__(self, map_file):
        self.tmx_data = load_pygame(map_file)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.width = self.tmx_data.width * self.tile_width
        self.height = self.tmx_data.height * self.tile_height

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render_to_surface()

    def render_to_surface(self):
        """
        Draw tiles onto the given surface.
        """
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):  # Ensure the layer has tile data
                for x, y, surf in layer.tiles():
                    pos = (x * self.tile_width, y * self.tile_height)
                    self.surface.blit(surf, pos)

    def get_surface(self):
        return self.surface

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Bear's Fishing Empire")

# Load map and add tiles
tile_map = TileMap("sources/maps/mapTest2.tmx")
map_surface = tile_map.get_surface()

# Group setup
sprite_group = CameraGroup(map_surface)


for i in range(20):
    random_x = random.randint(0,1000)
    random_y = random.randint(0,1000)
    Tree((random_x, random_y), sprite_group)


# Create player
Player((960, 590), sprite_group)

# Clock for delta time
fps = 120
clock = pygame.time.Clock()

running = True
while running:
    # Calculate delta time (time since last frame)
    dt = clock.tick(fps) / 1000.0  # Convert milliseconds to seconds

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear the screen
    screen.fill((134, 203, 146))

    # Update and draw sprites
    sprite_group.custom_draw()
    sprite_group.update(dt)
    

    # Flip the display
    pygame.display.flip()

pygame.quit()