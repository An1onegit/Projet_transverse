import pygame
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos : tuple, surf : pygame.surface, groups :pygame.sprite.Group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Player(pygame.sprite.Sprite):
    """
        This class represent the player. 
        It defines all the animations of the player's movements and record the inputs to handle movements.
    """
    def __init__(self, pos : tuple, groups : pygame.sprite.Group, hitboxes : list):
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
            for i in range(1, 8)
        ]

        self.down = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/down{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/down{i}.png").get_width() * scale_factor),
                int(pygame.image.load(f"sources/img/animations/down{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 8)
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
        self.speed = 200
        self.anim = 5
        self.hitboxes = hitboxes

    def movement_anim(self, direction : int):
        """ Animate the character in function of his movement direction """
        self.counter += .15
        match (direction):
            case 0:
                if self.counter >= len(self.right):
                    self.counter = 0
                self.image = self.right[int(self.counter)]
            case 1:
                if self.counter >= len(self.left):
                    self.counter = 0
                self.image = self.left[int(self.counter)]
            case 2:
                if self.counter >= len(self.down):
                    self.counter = 0
                self.image = self.down[int(self.counter)]
            case 3:
                if self.counter >= len(self.up):
                    self.counter = 0
                self.image = self.up[int(self.counter)]
            case 5:
                if self.counter >= len(self.idle):
                    self.counter = 0
                self.image = self.idle[int(self.counter)]

    def input(self):
        """ Record the keyboard input to move the player. """
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

    def update(self, dt):
        """ Handle the inputs, the collisions and the animations. """
        self.input()

        # Normalize diagonal movements
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # Prediction of the next position of the player 
        new_position = self.position + (self.direction * self.speed * dt)
        new_rect = self.rect.copy()
        new_rect.center = new_position

        # Check collision with a hitbox
        if not any(new_rect.colliderect(hitbox) for hitbox in self.hitboxes):
            self.position = new_position

        self.rect.center = self.position
        self.movement_anim(self.anim)

class CameraGroup(pygame.sprite.Group):
    """ Handle the camera to follow the player when he moves and """
    def __init__(self, surf):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

        # Ground
        self.ground_surf = surf
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        # Box setup
        self.camera_borders = {'left': 800, 'right': 800, 'top': 400, 'bottom': 400}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

    def box_target_camera(self, target):
        """
        Follow the player when it reaches the limit of the box.
        """
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

        # Creates the 3D illusion
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class TileMap:
    def __init__(self, map_file : str):
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
        """ Draw the map on the surface by rendering each tiles from each tile layer. """
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x * self.tile_width, y * self.tile_height)
                    self.surface.blit(surf, pos)

    def render_objects(self, sprite_group):
        """ Render all objects from the object layer 'trees'. """
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
        """ Load hitboxes objects from the 'hitboxes' layer. """
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