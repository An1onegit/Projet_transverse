import pygame
import random
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos : tuple, surf : pygame.surface, groups : pygame.sprite.Group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class Player(pygame.sprite.Sprite):
    """
    This class represents the player.
    It defines all the animations of the player's movements and handles movement input and collisions.
    """
    def __init__(self, pos: tuple, groups: pygame.sprite.Group, hitboxes: list):
        super().__init__(groups)
        scale_factor = 8

        self.right = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/right{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/right{i}.png").get_width() * scale_factor),
                 int(pygame.image.load(f"sources/img/animations/right{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 7)
        ]

        self.left = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/left{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/left{i}.png").get_width() * scale_factor),
                 int(pygame.image.load(f"sources/img/animations/left{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 7)
        ]

        self.up = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/up{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/up{i}.png").get_width() * scale_factor),
                 int(pygame.image.load(f"sources/img/animations/up{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 7)
        ]

        self.down = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/down{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/down{i}.png").get_width() * scale_factor),
                 int(pygame.image.load(f"sources/img/animations/down{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 7)
        ]

        self.idle = [
            pygame.transform.scale(
                pygame.image.load(f"sources/img/animations/idle{i}.png").convert_alpha(),
                (int(pygame.image.load(f"sources/img/animations/idle{i}.png").get_width() * scale_factor),
                 int(pygame.image.load(f"sources/img/animations/idle{i}.png").get_height() * scale_factor))
            )
            for i in range(1, 3)
        ]

        self.counter = 0
        self.image = self.idle[self.counter]
        self.rect = self.image.get_rect(topleft=pos)

        # Define the hitbox as the bottom half of the sprite
        hitbox_height = self.rect.height // 2
        self.hitbox = pygame.Rect(
            self.rect.left,
            self.rect.top + hitbox_height,
            self.rect.width,
            hitbox_height
        )

        self.position = pygame.math.Vector2(self.hitbox.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200 * 1.8
        self.anim = 5
        self.hitboxes = hitboxes
        self.sound_manager = SoundManager()
        self.walking_last_frame = False

    def movement_anim(self, direction: int):
        """ Animate the character based on movement direction """
        match direction:
            case 0:
                self.counter += .08
                if self.counter >= len(self.right):
                    self.counter = 0
                self.image = self.right[int(self.counter)]
            case 1:
                self.counter += .08
                if self.counter >= len(self.left):
                    self.counter = 0
                self.image = self.left[int(self.counter)]
            case 2:
                self.counter += .08
                if self.counter >= len(self.down):
                    self.counter = 0
                self.image = self.down[int(self.counter)]
            case 3:
                self.counter += .08
                if self.counter >= len(self.up):
                    self.counter = 0
                self.image = self.up[int(self.counter)]
            case 5:
                self.counter += .025
                if self.counter >= len(self.idle):
                    self.counter = 0
                self.image = self.idle[int(self.counter)]

    def input(self):
        """ Record keyboard input to move the player. """
        keys = pygame.key.get_pressed()
        moving = keys[pygame.K_z] or keys[pygame.K_q] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_UP]
        self.direction.x = 0
        self.direction.y = 0

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

        if moving:
            if not self.walking_last_frame:
                self.sound_manager.start_walk()
                self.walking_last_frame = True
        else:
            if self.walking_last_frame:
                self.sound_manager.stop_walk()
                self.walking_last_frame = False

    def check_interactions(self, interaction_zones):
        for zone in interaction_zones:
            if self.hitbox.colliderect(zone["rect"]):
                return zone
        return None

    def update(self, dt):
        """ Handle inputs, collisions, and animations. """
        self.input()

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        new_position = self.position + (self.direction * self.speed * dt)
        new_hitbox = self.hitbox.copy()
        new_hitbox.center = new_position

        if not any(new_hitbox.colliderect(hitbox) for hitbox in self.hitboxes):
            self.position = new_position

        self.hitbox.center = self.position
        self.rect.midbottom = self.hitbox.midbottom  # Align sprite to hitbox visually

        self.movement_anim(self.anim)

class CameraGroup(pygame.sprite.Group):
    """ Handle the camera to follow the player when he moves and create a 3D effect with objects. """
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
        self.camera_borders = {'left': self.display_surface.get_width() - 3/4*self.display_surface.get_width(), 'right': self.display_surface.get_width() - 3/4*self.display_surface.get_width(), 'top': self.display_surface.get_height() - 3/4*self.display_surface.get_height(), 'bottom': self.display_surface.get_height() - 3/4*self.display_surface.get_height()}
        print(self.camera_borders)
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

    def box_target_camera(self, target):
        """ Follow the player, but stop moving camera if it would go out of the map. """

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        # Calculate raw offset
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

        # CLAMP the camera offset to the map size
        self.offset.x = max(0, min(self.offset.x, self.ground_rect.width - self.display_surface.get_width()))
        self.offset.y = max(0, min(self.offset.y, self.ground_rect.height - self.display_surface.get_height()))


    def custom_draw(self, player):
        """ Draw the map with the '3D' objects. """
        self.box_target_camera(player)

        #ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # Creates the 3D illusion
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

            # # DEBUG: Draw camera box rectangle
            # debug_rect_color = (255, 0, 0)  # Red
            # debug_rect_thickness = 2

            # # Compute screen-space position of the camera_rect (relative to offset)
            # screen_camera_rect = pygame.Rect(
            #     self.camera_rect.left - self.offset.x,
            #     self.camera_rect.top - self.offset.y,
            #     self.camera_rect.width,
            #     self.camera_rect.height
            # )

            # pygame.draw.rect(self.display_surface, debug_rect_color, screen_camera_rect, debug_rect_thickness)

class TileMap:
    """ Render the map, objects and hitboxes. """
    def __init__(self, map_file : str):
        self.tmx_data = load_pygame(map_file)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.width = self.tmx_data.width * self.tile_width
        self.height = self.tmx_data.height * self.tile_height

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render_to_surface()

        self.display_surface = pygame.display.get_surface()

        xratio = self.display_surface.get_width() / 1920
        yration = self.display_surface.get_height() / 1080

        self.zoom = 4.5

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
                        scaled_image = pygame.transform.scale(
                            obj.image,
                            (int(obj.image.get_width() * self.zoom),
                            int(obj.image.get_height() * self.zoom))
                        )

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
    
    def load_interaction_zones(self):
        interaction_zones = []

        for obj in self.tmx_data.objects:
            if obj.type in ["fishing", "shop", "sell"]:
                interaction = {
                    "rect": pygame.Rect(
                        int(obj.x * self.zoom), 
                        int(obj.y * self.zoom), 
                        int(obj.width * self.zoom), 
                        int(obj.height * self.zoom)
                    ),
                    "type": obj.type,
                    "name": obj.name,
                    "message": obj.properties.get("message", "Press E to interact"),
                }
                interaction_zones.append(interaction)

        return interaction_zones

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Background music
        self.music_tracks = {
            "forest": "sources/sounds/ambient.mp3",
        }

        # Sound Effects (multiple variants per action)
        self.sfx = {
            "walk": [
                pygame.mixer.Sound("sources/sounds/Walk1.wav"),
                pygame.mixer.Sound("sources/sounds/Walk2.wav")
            ],
            "splash": [
                pygame.mixer.Sound("sources/sounds/Splash1.wav"),
                pygame.mixer.Sound("sources/sounds/Splash2.wav"),
                pygame.mixer.Sound("sources/sounds/Splash3.wav")
            ],
            "money": [pygame.mixer.Sound("sources/sounds/Money.wav")],
        }

        # Set volumes
        for sound_list in self.sfx.values():
            for sound in sound_list:
                sound.set_volume(0.8)

        self.walking_channel = None  # Separate channel for walking loop
        self.walking = False

    def play_music(self, name, loop=True, volume=0.5):
        if name in self.music_tracks:
            pygame.mixer.music.load(self.music_tracks[name])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def play_sfx(self, name):
        """Play a random sound from the given category."""
        if name in self.sfx:
            sound = random.choice(self.sfx[name])
            sound.play()

    def start_walk(self):
        if not self.walking:
            sound = self.sfx["walk"][random.randint(0,1)]
            self.walking_channel = sound.play(loops=-1)
            self.walking = True

    def stop_walk(self):
        if self.walking and self.walking_channel:
            self.walking_channel.stop()
            self.walking = False

def draw_text(text, font, text_col, x, y, screen, center=False):
    img = font.render(text, True, text_col)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))