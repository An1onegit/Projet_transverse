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
        self.width, self.height = screen.get_size()
        self.inventory = inventory
        self.camera_offset_x = 0
        self.waiting_for_restart = False
        self.last_caught_fish_text = None
        self.reset()

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
        self.fishing_game = FishingMiniGame(self.screen, self.font, self)
        self.thrown = False
        self.angle_timer = 0.0
        self.strength_timer = 0.0
        self.aiming_angle = True
        self.angle_deg = 0
        self.charge_strength = 0
        self.camera_offset_x = 0

    def handle_input(self, event):
        if self.waiting_for_restart:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.waiting_for_restart = False
                self.reset()
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

                if abs(self.vy) < 100 or self.bounces > MAX_BOUNCES:
                    self.throwing = False
                    if hit_water:
                        self.fishing_game.start()

            self.camera_offset_x = self.projectile_position[0] - self.width // 2

        for splash in self.splashes:
            splash.update(dt)
        self.splashes = [s for s in self.splashes if s.life > 0]

        self.fishing_game.update(dt, keys)

    def reset_game(self):
        return self.reset()

    def get_fish(self):
        if not self.inventory:
            print("No inventory linked!")
            return

        distance = self.projectile_position[0] - self.launch_x
        if distance < 0:
            distance = 0

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

        self.last_caught_fish_text = f"You caught a {self.fish_name} ({rarity})!\nPress SPACE to fish again!"
        self.waiting_for_restart = True

    def draw(self):
        offset = self.camera_offset_x if self.throwing or self.fishing_game.active else 0

        self.screen.fill((135, 206, 235))

        bay_width = self.water_start_x
        pygame.draw.rect(self.screen, (34, 139, 34), (-offset - self.width * 2, self.ground_level, bay_width + self.width * 2, self.height - self.ground_level))

        pygame.draw.line(self.screen, (0, 80, 100), (self.water_start_x - offset, self.ground_level), (self.water_start_x - offset, self.height), 3)
        pygame.draw.rect(self.screen, (0, 105, 148), (self.water_start_x - offset, self.ground_level, self.width * 5, self.height - self.ground_level))

        pygame.draw.circle(self.screen, (0, 0, 0), (self.launch_x - offset, int(self.launch_y)), 6)

        if not self.throwing and not self.fishing_game.active:
            if self.aiming_angle:
                current_angle = abs(math.sin(self.angle_timer * 2)) * 80 + 5
                angle_rad = math.radians(current_angle)
            else:
                current_angle = self.angle_deg
                current_strength = abs(math.sin(self.strength_timer * 2)) * self.max_strength

                bar_x = self.launch_x - 50 - offset
                bar_y = self.launch_y + 40
                bar_width = 150
                bar_height = 20
                fill_width = int((current_strength / self.max_strength) * bar_width)
                pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)
                pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, fill_width, bar_height))
                self.screen.blit(self.font.render("Strength", True, (0, 0, 0)), (bar_x, bar_y - 25))

                angle_rad = math.radians(current_angle)

            line_len = int(self.height * 0.2)
            end_x = self.launch_x + math.cos(angle_rad) * line_len - offset
            end_y = self.launch_y - math.sin(angle_rad) * line_len
            pygame.draw.line(self.screen, (0, 0, 0), (self.launch_x - offset, self.launch_y), (end_x, end_y), 2)
            self.screen.blit(self.font.render(f"Angle: {int(current_angle)}°", True, (0, 0, 0)), (self.launch_x - offset - 50, self.launch_y - 60))

        if self.projectile_position:
            pygame.draw.circle(self.screen, (255, 50, 50), (int(self.projectile_position[0]) - offset, int(self.projectile_position[1])), 6)
            distance = max(0, int(self.projectile_position[0] - self.launch_x))
            distance_text = self.font.render(f"Distance: {distance}px", True, (0, 0, 0))
            self.screen.blit(distance_text, (self.width - distance_text.get_width() - 250, 140))

        for splash in self.splashes:
            splash_x = int(splash.x - offset)
            splash_y = int(splash.y)
            pygame.draw.circle(self.screen, (255, 255, 255), (splash_x, splash_y), 2)

        self.fishing_game.draw()

        if self.waiting_for_restart and self.last_caught_fish_text:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            lines = self.last_caught_fish_text.split('\n')
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 50))
                self.screen.blit(text_surface, text_rect)
            self.screen.blit(self.fish_images[self.fish_name], (self.width // 2 - self.fish_images[self.fish_name].get_width() // 2, self.height // 2 + 150))