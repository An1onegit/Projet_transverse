import pygame
import math
import random

# Constants
GRAVITY = 9.81 * 50
ENERGY_LOSS_FACTOR = 0.7
MAX_BOUNCES = 3
FISH_GAME_TIME = 15
FISH_BAR_SPEED = 300

# Fish tiers
FISH_TIERS = {
    "Common": ["Small Carp", "Tiny Bass", "Minnow"],
    "Uncommon": ["Bluegill", "Pike", "Perch"],
    "Rare": ["Golden Trout", "Catfish", "Silver Salmon"],
    "Epic": ["Giant Tuna", "Swordfish", "Mahi-Mahi"],
    "Legendary": ["Ancient Coelacanth", "Mythical Leviathan", "Rainbow Koi"]
}


# Splash particle class
class SplashParticle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = 1.0

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.dy += GRAVITY * dt * 0.5
        self.life -= dt * 2

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 2)

# Fishing minigame
class FishingMiniGame:
    def __init__(self, screen, font, fishing_game):
        self.screen = screen
        self.font = font
        self.width, self.height = screen.get_size()

        self.bar_width = int(self.width * 0.1)
        self.bar_height = int(self.height * 0.04)
        self.cursor_width = int(self.bar_width * 0.05)

        self.min_x = int(self.width * 0.3)
        self.max_x = int(self.width * 0.7)
        self.cursor_x = self.min_x
        self.cursor_speed = 0
        self.fish_x = random.randint(self.min_x, self.max_x - self.bar_width)

        self.bar_fill = 0.0
        self.bar_direction = 1
        self.success = False
        self.total_time = FISH_GAME_TIME  # Starting time for the countdown
        self.active = False

        self.fishing_game = fishing_game

    def start(self):
        self.active = True
        self.total_time = FISH_GAME_TIME  # Reset time
        self.success = False
        self.cursor_x = self.min_x
        self.fish_x = random.randint(self.min_x, self.max_x - self.bar_width)
        self.bar_fill = 0.0

    def update(self, dt, keys):
        if not self.active:
            return

        self.total_time -= dt  # Subtract delta time from total time

        if self.total_time <= 0:
            self.active = False  # End the game when time runs out
            self.fishing_game.get_fish()  # Give the fish (or handle accordingly)

        if keys[pygame.K_SPACE]:
            self.cursor_speed += 7300 * dt
        else:
            self.cursor_speed -= 7300 * dt

        self.cursor_x += self.cursor_speed * dt
        self.cursor_speed *= 0.9
        self.cursor_x = max(self.min_x, min(self.max_x, self.cursor_x))

        self.fish_x += FISH_BAR_SPEED * self.bar_direction * dt
        if self.fish_x < self.min_x or self.fish_x > self.max_x - self.bar_width:
            self.bar_direction *= -1

        in_bar = self.fish_x <= self.cursor_x <= self.fish_x + self.bar_width
        if in_bar:
            self.bar_fill += dt * 0.5
        else:
            self.bar_fill -= dt * 0.3

        self.bar_fill = max(0.0, min(1.0, self.bar_fill))

        if self.bar_fill >= 1.0:
            self.success = True
            self.active = False
            self.fishing_game.get_fish()

    def draw(self):
        if not self.active:
            return

        y_pos = int(self.height * 0.2)
        fill_bar_y = int(self.height * 0.3)

        pygame.draw.rect(self.screen, (30, 30, 30), (self.fish_x, y_pos, self.bar_width, self.bar_height))
        pygame.draw.rect(self.screen, (200, 200, 0), (self.cursor_x, y_pos, self.cursor_width, self.bar_height))

        fill_width = int((self.max_x - self.min_x) * self.bar_fill)
        pygame.draw.rect(self.screen, (100, 255, 100), (self.min_x, fill_bar_y, fill_width, 30))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.min_x, fill_bar_y, self.max_x - self.min_x, 30), 2)

        self.screen.blit(self.font.render("Fishing...", True, (0, 0, 0)), (self.min_x, fill_bar_y + 40))

        # Display the countdown timer
        timer_text = self.font.render(f"Time Left: {int(self.total_time)}s", True, (0,0,0))
        self.screen.blit(timer_text, (self.width // 2 - timer_text.get_width() // 2, fill_bar_y + 40))


# Main Fishing Game
class FishingGame:
    def __init__(self, screen, font, inventory, fish_images, max_strength=1000):
        self.screen = screen
        self.font = font
        self.fish_images = fish_images
        self.max_strength = max_strength
        self.width, self.height = screen.get_size() # <--- Screen dimensions used here
        self.inventory = inventory
        self.camera_offset_x = 0
        self.waiting_for_restart = False
        self.last_caught_fish_text = None

    
        self.background_image_path = "sources/img/test_image.jpg" 

        try:
            original_background = pygame.image.load(self.background_image_path).convert()
            original_width, original_height = original_background.get_size()
            print(f"Successfully loaded original background: {self.background_image_path} ({original_width}x{original_height})")

            # 2. Calculate new width to maintain aspect ratio based on SCREEN height
            if original_height > 0: # Avoid division by zero
                aspect_ratio = original_width / original_height
                # Calculate the width needed if the height is scaled to match the screen height
                scaled_width = int(self.height * aspect_ratio)
                scaled_height = self.height # Target height is the screen height
            else:
                 # Handle case of image with 0 height? Use original width, screen height.
                scaled_width = original_width
                scaled_height = self.height

            # 3. Scale the image to the new dimensions (matching screen height)
            self.background_image = pygame.transform.scale(original_background, (scaled_width, scaled_height))

            # 4. Store the SCALED dimensions for tiling calculations
            self.bg_width = self.background_image.get_width() # This is scaled_width
            self.bg_height = self.background_image.get_height() # This is scaled_height (== self.height)
            print(f"Background scaled to fit screen height: {self.bg_width}x{self.bg_height}")

        except pygame.error as e:
            print(f"!!! ERROR LOADING/SCALING BACKGROUND IMAGE: {e}")
            print(f"!!! Failed operation for: {self.background_image_path}")
            print("!!! Using fallback blue color instead.")
            # Fallback: Create a surface matching screen size if image fails
            self.background_image = pygame.Surface((self.width, self.height))
            self.background_image.fill((135, 206, 235)) # Old blue color
            # Set bg dimensions to screen size for the fallback
            self.bg_width = self.width
            self.bg_height = self.height

        self.reset() # Call reset after loading/scaling the background


    def reset(self):
        self.projectile_position = None
        self.vx = 0
        self.vy = 0

        self.ground_level = self.height - int(self.height * 0.2)
        self.water_start_x = self.width // 2
        self.launch_x = int(self.width * 0.2)
        self.launch_y = self.ground_level - 10

        self.angle = 0
        self.v0 = 1000
        self.throwing = False
        self.bounces = 0
        self.splashes = []
        # Ensure the minigame instance is created (if needed on reset, but usually done in init)
        if not hasattr(self, 'fishing_game'): # Safety check
            self.fishing_game = FishingMiniGame(self.screen, self.font, self)
        else:
            self.fishing_game.active = False # Ensure minigame isn't active after reset

        self.thrown = False
        self.angle_timer = 0.0
        self.strength_timer = 0.0
        self.aiming_angle = True
        self.angle_deg = 0
        self.charge_strength = 0
        self.camera_offset_x = 0
        # Reset waiting state etc.
        self.waiting_for_restart = False
        self.last_caught_fish_text = None


    def handle_input(self, event):
        if self.waiting_for_restart:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Don't reset background here, just game state
                self.waiting_for_restart = False
                # Reset only the dynamic game elements
                self.projectile_position = None
                self.vx = 0; self.vy = 0
                self.throwing = False; self.thrown = False
                self.bounces = 0; self.splashes.clear()
                self.fishing_game.active = False # Ensure minigame isn't active
                self.aiming_angle = True; self.angle_timer = 0.0; self.strength_timer = 0.0
                self.camera_offset_x = 0
                self.last_caught_fish_text = None
            return

        if not self.throwing and not self.fishing_game.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.aiming_angle:
                        self.angle_deg = abs(math.sin(self.angle_timer * 2)) * 80 + 5
                        self.aiming_angle = False
                        self.angle_timer = 0.0
                    else:
                        self.charge_strength = abs(math.sin(self.strength_timer * 2)) * self.max_strength
                        self.start_throw()

    def start_throw(self):
        angle_rad = math.radians(self.angle_deg)
        self.vx = self.charge_strength * math.cos(angle_rad)
        self.vy = -self.charge_strength * math.sin(angle_rad)
        self.projectile_position = [self.launch_x, self.launch_y]
        self.throwing = True
        self.bounces = 0
        self.splashes.clear()
        self.thrown = True

    def update(self, dt):
        if self.waiting_for_restart:
            return

        keys = pygame.key.get_pressed()

        if not self.throwing and not self.fishing_game.active:
            if self.aiming_angle:
                self.angle_timer += dt
            else:
                self.strength_timer += dt

        if self.throwing and self.projectile_position:
            self.vy += GRAVITY * dt
            self.projectile_position[0] += self.vx * dt
            self.projectile_position[1] += self.vy * dt

            x, y = self.projectile_position
            hit_ground = y >= self.ground_level
            hit_water = x > self.water_start_x and y >= self.ground_level

            if hit_ground:
                self.projectile_position[1] = self.ground_level
                self.bounces += 1

                if hit_water:
                    for _ in range(10):
                        dx = random.uniform(-100, 100)
                        dy = random.uniform(-300, -100)
                        self.splashes.append(SplashParticle(x, self.ground_level, dx, dy))

                self.vy = -self.vy * ENERGY_LOSS_FACTOR
                self.vx = self.vx * ENERGY_LOSS_FACTOR

                # Stop condition check
                if abs(self.vy) < 50 or self.bounces > MAX_BOUNCES: # Reduced vy threshold slightly
                    self.throwing = False
                    if hit_water:
                        # Only start if we landed IN water and stopped
                        self.fishing_game.start()
                    else:
                        # If we stopped on land, prepare for restart immediately
                        self.last_caught_fish_text = "Landed on shore... Try again!\nPress ENTER to fish again!"
                        self.waiting_for_restart = True


            # Update camera offset based on projectile position
            # Keep camera centered on projectile, but don't scroll left past the start area
            target_offset = self.projectile_position[0] - self.width * 0.3 # Keep projectile around 30% mark
            self.camera_offset_x = max(0, target_offset) # Prevent scrolling left past launch area


        for splash in self.splashes:
            splash.update(dt)
        self.splashes = [s for s in self.splashes if s.life > 0]

        self.fishing_game.update(dt, keys)

    def reset_game(self):
        # This might be called externally, ensure it resets properly
        self.reset() # Full reset including background (though it's static)

    def get_fish(self):
        if not self.inventory:
            print("No inventory linked!")
            self.last_caught_fish_text = "Error: No inventory!\nPress ENTER to try again!"
            self.waiting_for_restart = True
            return

        # Calculate distance only if projectile exists (might not if time ran out)
        distance = 0
        if self.projectile_position:
             distance = self.projectile_position[0] - self.water_start_x
             if distance < 0: distance = 0 # If somehow landed before water starts

        if not self.fishing_game.success and self.fishing_game.total_time <=0:
             # Handle time running out scenario
             self.last_caught_fish_text = "Ran out of time!\nPress ENTER to fish again!"
             self.waiting_for_restart = True
             return # Don't award fish if time ran out


        # Determine rarity based on distance
        if distance < 600:
            rarity = "Common"
        elif distance < 1200:
            rarity = "Uncommon"
        elif distance < 2000:
            rarity = "Rare"
        elif distance < 3000:
            rarity = "Epic"
        else:
            rarity = "Legendary"

        self.fish_name = random.choice(FISH_TIERS[rarity])
        self.inventory.add_fish(self.fish_name)

        self.last_caught_fish_text = f"You caught a {self.fish_name} ({rarity})!\nPress ENTER to fish again!"
        self.waiting_for_restart = True


    def draw(self):
        # Use integer offset for drawing calculations
        offset = int(self.camera_offset_x) if self.throwing or self.fishing_game.active else 0


        # Calculate the starting X coordinate for tiling based on the offset
        start_x = -(offset % self.bg_width) # Use the possibly scaled width

        # Tile the background image (vertically, it should only need one tile now)
        for y in range(0, self.height, self.bg_height): # self.bg_height == self.height now
            for x in range(start_x, self.width, self.bg_width):
                self.screen.blit(self.background_image, (x, y))


        # --- Draw Ground and Water (relative to offset) ---
        # Draw ground slightly wider to avoid gaps when scrolling
        ground_draw_width = self.water_start_x + self.width * 2 # Make sure ground covers screen area
        pygame.draw.rect(self.screen, (34, 139, 34), (-offset, self.ground_level, ground_draw_width, self.height - self.ground_level))

        # Draw water wider as well
        water_draw_width = self.width * 5 # Arbitrarily large width
        pygame.draw.rect(self.screen, (0, 105, 148), (self.water_start_x - offset, self.ground_level, water_draw_width, self.height - self.ground_level))

        pygame.draw.line(self.screen, (0, 80, 100), (self.water_start_x - offset, self.ground_level), (self.water_start_x - offset, self.height), 3)


        # --- Draw Player/Launch Point (relative to offset) ---
        pygame.draw.circle(self.screen, (0, 0, 0), (self.launch_x - offset, int(self.launch_y)), 6)

        # --- Draw Aiming UI (relative to offset) ---
        if not self.throwing and not self.fishing_game.active and not self.waiting_for_restart:
            current_angle = 0 
            if self.aiming_angle:
                current_angle = abs(math.sin(self.angle_timer * 2)) * 80 + 5
                angle_rad = math.radians(current_angle)
            else: # Charging strength phase
                current_angle = self.angle_deg # Use the locked angle
                current_strength = abs(math.sin(self.strength_timer * 2)) * self.max_strength

                bar_x = self.launch_x - 50 - offset
                bar_y = self.launch_y + 40
                bar_width = 150
                bar_height = 20
                fill_width = int((current_strength / self.max_strength) * bar_width)

                # Draw strength bar background/border first
                pygame.draw.rect(self.screen, (50, 50, 50), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4)) # Optional border
                pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height)) # Background for unfilled part
                pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, fill_width, bar_height)) # Filled part

                # Render text with background for better visibility
                strength_text = self.font.render("Strength", True, (255, 255, 255), (0,0,0)) # White text, black bg
                self.screen.blit(strength_text, (bar_x, bar_y - 25))

                angle_rad = math.radians(current_angle)

            # Draw aiming line
            line_len = int(self.height * 0.15) # Shorter line maybe
            end_x = self.launch_x + math.cos(angle_rad) * line_len - offset
            end_y = self.launch_y - math.sin(angle_rad) * line_len
            pygame.draw.line(self.screen, (0, 0, 0), (self.launch_x - offset, self.launch_y), (end_x, end_y), 3) # Thicker line

            # Render angle text with background
            angle_val_text = f"Angle: {int(current_angle)}°"
            angle_surf = self.font.render(angle_val_text, True, (255, 255, 255), (0,0,0)) # White text, black bg
            self.screen.blit(angle_surf, (self.launch_x - offset - 50, self.launch_y - 60))


        # --- Draw Projectile (relative to offset) ---
        if self.projectile_position:
             proj_x = int(self.projectile_position[0]) - offset
             proj_y = int(self.projectile_position[1])
             pygame.draw.circle(self.screen, (255, 50, 50), (proj_x, proj_y), 6)

             # Display distance only when projectile is active
             distance = max(0, int(self.projectile_position[0] - self.water_start_x))
             distance_text_surf = self.font.render(f"Distance: {distance}px", True, (255, 255, 255), (0,0,0)) # White text, black bg
             # Position distance text top-right
             self.screen.blit(distance_text_surf, (self.width - distance_text_surf.get_width() - 20, 20))


        # --- Draw Splashes (relative to offset) ---
        for splash in self.splashes:
            # Use the splash particle's draw method, but pass the offset
            splash_x = int(splash.x - offset)
            splash_y = int(splash.y)
            if splash.life > 0: # Check life before drawing
                 # Draw manually here since SplashParticle.draw doesn't take offset
                 pygame.draw.circle(self.screen, (255, 255, 255), (splash_x, splash_y), 2)


        # --- Draw Fishing Minigame UI (Not relative to offset - fixed position) ---
        self.fishing_game.draw() # This draws the minigame bar etc.

        # --- Draw Restart Overlay ---
        if self.waiting_for_restart and self.last_caught_fish_text:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA) # Use SRCALPHA for transparency
            overlay.fill((0, 0, 0, 180))  # Black with alpha (0-255)
            self.screen.blit(overlay, (0, 0))

            lines = self.last_caught_fish_text.split('\n')
            text_y = self.height // 2 - (len(lines) * 40) // 2 # Start Y to center block

            # Draw fish image if a fish was caught (check fish_name exists and is in fish_images)
            fish_image_to_draw = None
            if hasattr(self, 'fish_name') and self.fish_name and self.fish_name in self.fish_images:
                 fish_image_to_draw = self.fish_images[self.fish_name]
                 # Adjust text Y position to make room for image below
                 text_y -= fish_image_to_draw.get_height() // 3 # Move text up a bit


            # Draw text lines
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, (255, 255, 255)) # White text
                text_rect = text_surface.get_rect(center=(self.width // 2, text_y + i * 40))
                self.screen.blit(text_surface, text_rect)

            # Draw fish image below text if available
            if fish_image_to_draw:
                 img_x = self.width // 2 - fish_image_to_draw.get_width() // 2
                 img_y = text_y + len(lines) * 40 # Position below the last line of text
                 self.screen.blit(fish_image_to_draw, (img_x, img_y))