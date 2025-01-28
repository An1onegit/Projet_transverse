import pygame
import math
from pytmx.util_pygame import load_pygame
<<<<<<< HEAD
=======
from library.menu import *
>>>>>>> parent of a82304d (update)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

<<<<<<< HEAD
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("sources/img/rpgChar.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image,.8)
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 300  # Movement speed in pixels per second
=======
>>>>>>> parent of a82304d (update)


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

<<<<<<< HEAD
class CameraGroup(pygame.sprite.Group):
    def __init__(self, surf):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

        #Ground
        self.ground_surf = surf
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        #box setup
        self.camera_borders = {'left': 800, 'right': 800, 'top': 400, 'bottom': 400}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)


    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, player):

        self.box_target_camera(player)

        #ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
=======
        # Update the position
        x += x_change * speed * dt
        y += y_change * speed * dt

        # RENDER YOUR GAME HERE
        sprite_group.draw(screen)

        pygame.draw.rect(screen,(57, 42, 22),(x,y,width,height))
>>>>>>> parent of a82304d (update)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(fps)  # limits FPS to 60

<<<<<<< HEAD
        self.zoom = 2.5

    def render_to_surface(self):
        """
        Draw tiles onto the given surface.
        """
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):  # Ensure the layer has tile data
                for x, y, surf in layer.tiles():
                    pos = (x * self.tile_width, y * self.tile_height)
                    self.surface.blit(surf, pos)

    def render_objects(self):
        for obj in self.tmx_data.objects:
            if obj.image:
                # Scale the object's image
                scaled_image = pygame.transform.scale(
                    obj.image,
                    (int(obj.image.get_width() * self.zoom),
                     int(obj.image.get_height() * self.zoom))
                )

                # Scale the object's position
                scaled_pos = (obj.x * self.zoom, obj.y * self.zoom)

                # Create the object
                Tile(scaled_pos, surf=scaled_image, groups=sprite_group)

    def get_surface(self):
        return self.surface

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Bear's Fishing Empire")

# Load map and add tiles
tile_map = TileMap("sources/maps/mapTest2.tmx")
map_surface = tile_map.get_surface().convert_alpha()
map_surface = pygame.transform.scale_by(map_surface, tile_map.zoom)

# Group setup
sprite_group = CameraGroup(map_surface)

tile_map.render_objects()

# Create player
player = Player((960, 590), sprite_group)

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
    sprite_group.custom_draw(player)
    sprite_group.update(dt)


    # Flip the display
    pygame.display.flip()

pygame.quit()
=======
    pygame.quit()

    
if MainMenu():
    Main()
>>>>>>> parent of a82304d (update)
