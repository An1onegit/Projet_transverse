import pygame
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, hitboxes):
        super().__init__(groups)
        scale_factor = 4

        self.right = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/right{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/right{i}.png").get_width() * scale_factor),
                int(pygame.image.load(f"sources/img/animations/right{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 5)
        ]

        self.left = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/left{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/left{i}.png").get_width() * scale_factor),
                int(pygame.image.load(f"sources/img/animations/left{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 5)
        ]

        self.up = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/up{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/up{i}.png").get_width() * scale_factor),
                int(pygame.image.load(f"sources/img/animations/up{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 5)
        ]

        self.down = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/down{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/down{i}.png").get_width() * scale_factor),
                int(pygame.image.load(f"sources/img/animations/down{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 5)
        ]

        self.idle = [
            pygame.transform.scale(
                pygame.image.load("sources/img/animations/down1.png").convert_alpha(),
                (int(pygame.image.load("sources/img/animations/down1.png").get_width() * scale_factor),
                int(pygame.image.load("sources/img/animations/down1.png").get_height() * scale_factor))
            )
        ]

        self.counter = 0
        self.image = self.idle[self.counter]
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 300  # Movement speed in pixels per second
        self.anim = 5
        self.hitboxes = hitboxes

    def movement_anim(self, direction):
        match (direction):
            case 0:
                self.counter += .15
                if self.counter >= len(self.right):
                    self.counter = 0
                self.image = self.right[int(self.counter)]
            case 1:
                self.counter += .15
                if self.counter >= len(self.left):
                    self.counter = 0
                self.image = self.left[int(self.counter)]
            case 2:
                self.counter += .15
                if self.counter >= len(self.down):
                    self.counter = 0
                self.image = self.down[int(self.counter)]
            case 3:
                self.counter += .15
                if self.counter >= len(self.up):
                    self.counter = 0
                self.image = self.up[int(self.counter)]
            case 5:
                self.counter += .15
                if self.counter >= len(self.idle):
                    self.counter = 0
                self.image = self.idle[int(self.counter)]
            

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        # Handle key inputs
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.anim = 0
        elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.anim = 1
        

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.anim = 2

        elif keys[pygame.K_z] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.anim = 3

    def check_collision(self):
        """ Prevent movement if hitting a hitbox """
        for hitbox in self.hitboxes:
            if self.rect.colliderect(hitbox):
                return True  # Colliding
        return False  # No collision
        

    def update(self, dt):
        self.input()
        # Normalize diagonal movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            
        new_position = self.position + (self.direction * self.speed * dt)
        new_rect = self.rect.copy()
        new_rect.center = new_position

        if not any(new_rect.colliderect(hitbox) for hitbox in self.hitboxes):
            self.position = new_position  # Move only if no collision

        self.rect.center = self.position
        self.movement_anim(self.anim)

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

class TileMap:
    def __init__(self, map_file):
        self.tmx_data = load_pygame(map_file)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.width = self.tmx_data.width * self.tile_width
        self.height = self.tmx_data.height * self.tile_height

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render_to_surface()

        self.zoom = 2.5

        self.hitboxes = []

        self.load_hitboxes()

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
        for layer in self.tmx_data.layers:
            if layer.name == "trees":
                for obj in layer:
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

    def load_hitboxes(self):
        """ Load hitbox objects from the 'hitboxes' layer in Tiled """
        for layer in self.tmx_data.layers:
            if layer.name == "hitboxes":
                for obj in layer:
                    hitbox_rect = pygame.Rect(
                        int(obj.x * self.zoom), 
                        int(obj.y * self.zoom), 
                        int(obj.width * self.zoom), 
                        int(obj.height * self.zoom)
                    )
                    self.hitboxes.append(hitbox_rect)

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
player = Player((960, 590), sprite_group, tile_map.hitboxes)

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
        else:
            player.anim = 5

    # Clear the screen
    screen.fill((134, 203, 146))

    # Update and draw sprites
    sprite_group.custom_draw(player)
    sprite_group.update(dt)


    # Flip the display
    pygame.display.flip()

pygame.quit()