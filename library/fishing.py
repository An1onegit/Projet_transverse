import pygame
import math
import random

GRAVITY = 9.81 * 50
ENERGY_LOSS_FACTOR = 0.7
MAX_BOUNCES = 3
FISH_GAME_TIME = 30
FISH_BAR_SPEED = 300

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

class FishingMiniGame:
    def __init__(self, screen, font):
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
        self.total_time = 0
        self.active = False

    def start(self):
        self.active = True
        self.total_time = 0
        self.success = False
        self.cursor_x = self.min_x
        self.fish_x = random.randint(self.min_x, self.max_x - self.bar_width)
        self.bar_fill = 0.0

    def update(self, dt, keys):
        if not self.active:
            return

        self.total_time += dt
        if self.total_time > FISH_GAME_TIME:
            self.active = False
            return

        if keys[pygame.K_SPACE]:
            self.cursor_speed += 10000 * dt
        else:
            self.cursor_speed -= 8500 * dt

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
        if self.success:
            self.screen.blit(self.font.render("You caught a fish!", True, (0, 100, 0)), (self.min_x, fill_bar_y + 80))

class FishingGame:
    def __init__(self, screen, font, max_strength=2000):
        self.screen = screen
        self.font = font
        self.max_strength = max_strength
        self.width, self.height = screen.get_size()
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
        self.fishing_game = FishingMiniGame(self.screen, self.font)
        self.thrown = False
        self.angle_timer = 0.0
        self.strength_timer = 0.0
        self.aiming_angle = True
        self.angle_deg = 0
        self.charge_strength = 0

    def reset_game(self):
        self.reset()

    def handle_input(self, event):
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

        for splash in self.splashes:
            splash.update(dt)
        self.splashes = [s for s in self.splashes if s.life > 0]

        self.fishing_game.update(dt, keys)

    def draw(self):
        self.screen.fill((135, 206, 235))
        pygame.draw.rect(self.screen, (34, 139, 34), (0, self.ground_level, self.water_start_x, self.height - self.ground_level))
        pygame.draw.rect(self.screen, (0, 105, 148), (self.water_start_x, self.ground_level, self.width - self.water_start_x, self.height - self.ground_level))

        pygame.draw.circle(self.screen, (0, 0, 0), (self.launch_x, int(self.launch_y)), 6)

        if not self.throwing and not self.fishing_game.active:
            if self.aiming_angle:
                current_angle = abs(math.sin(self.angle_timer * 2)) * 80 + 5
                angle_rad = math.radians(current_angle)
            else:
                current_angle = self.angle_deg
                current_strength = abs(math.sin(self.strength_timer * 2)) * self.max_strength

                # Draw strength bar near launcher
                bar_x = self.launch_x - 50
                bar_y = self.launch_y + 40
                bar_width = 150
                bar_height = 20
                fill_width = int((current_strength / self.max_strength) * bar_width)
                pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)
                pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, fill_width, bar_height))
                self.screen.blit(self.font.render("Strength", True, (0, 0, 0)), (bar_x, bar_y - 25))

                angle_rad = math.radians(current_angle)

            line_len = int(self.height * 0.2)
            end_x = self.launch_x + math.cos(angle_rad) * line_len
            end_y = self.launch_y - math.sin(angle_rad) * line_len
            pygame.draw.line(self.screen, (0, 0, 0), (self.launch_x, self.launch_y), (end_x, end_y), 2)
            self.screen.blit(self.font.render(f"Angle: {int(current_angle)}°", True, (0, 0, 0)), (self.launch_x - 50, self.launch_y - 60))

        if self.projectile_position:
            pygame.draw.circle(self.screen, (255, 50, 50), (int(self.projectile_position[0]), int(self.projectile_position[1])), 6)

        for splash in self.splashes:
            splash.draw(self.screen)

        self.fishing_game.draw()