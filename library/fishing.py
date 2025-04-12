import pygame
import math

class FishingGame:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.reset_game()

    def reset_game(self):
        # Game state
        self.game_started = False
        self.power_selected = False
        self.angle_selected = False

        # Launch power
        self.power_bar_height = 200
        self.power_bar_y = 200
        self.power_cursor_y = self.power_bar_y
        self.power_speed = 5
        self.power_direction = 1

        # Throw angle
        self.angle = 0
        self.angle_speed = 0.03
        self.angle_max = math.pi / 2
        self.angle_min = 0

        # Throw data
        self.power = 0
        self.v0 = 0
        self.angle_value = 0
        self.projectile_position = None
        self.impact_position = None
        self.vx = 0
        self.vy = 0
        self.launch_y = 0
        self.launch_x = 400
        self.gravity = 9.81 * 50  # 50 pixels = 1 meter
        self.landing_distance = None

        self.ground_level = self.screen.get_height() - 200
        self.throw_power = 800

    def draw_background(self):
        self.screen.fill((0, 100, 255))  # Blue sky
        pygame.draw.rect(self.screen, (0, 200, 0), (0, self.ground_level, self.screen.get_width(), self.screen.get_height()))  # Green ground

    def draw_power_bar(self):
        pygame.draw.rect(self.screen, (200, 0, 0), (500, self.power_bar_y, 300, self.power_bar_height // 3))
        pygame.draw.rect(self.screen, (255, 255, 0), (500, self.power_bar_y + self.power_bar_height // 3, 300, self.power_bar_height // 3))
        pygame.draw.rect(self.screen, (0, 200, 0), (500, self.power_bar_y + 2 * self.power_bar_height // 3, 300, self.power_bar_height // 3))
        pygame.draw.rect(self.screen, (255, 255, 255), (450, self.power_cursor_y, 400, 10))

    def draw_angle_arc(self):
        pygame.draw.arc(self.screen, (150, 150, 150), (300, 350, 200, 100), self.angle_min, self.angle_max, 5)
        end_x = 400 + 100 * math.cos(self.angle)
        end_y = 400 - 50 * math.sin(self.angle)
        pygame.draw.line(self.screen, (255, 255, 255), (400, 400), (end_x, end_y), 4)

    def draw_trajectory(self):
        trajectory_positions = []
        temp_vx = self.v0 * math.cos(self.angle_value)
        temp_vy = -self.v0 * math.sin(self.angle_value)
        temp_x = self.launch_x
        temp_y = self.launch_y

        # Generate points along the trajectory
        for t in range(1, 100):
            # Simple physics calculations
            time = t * 0.05  # Time step
            x = temp_x + temp_vx * time
            y = temp_y + temp_vy * time + 0.5 * self.gravity * time ** 2

            if y >= self.ground_level:
                break  # Stop once the projectile hits the ground

            trajectory_positions.append((x, y))

        # Draw the trajectory as a series of circles or a line
        for pos in trajectory_positions:
            pygame.draw.circle(self.screen, (255, 255, 0), (int(pos[0]), int(pos[1])), 3)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.game_started:
                    self.game_started = True
                    self.launch_y = self.ground_level - 10
                    self.projectile_position = [self.launch_x, self.launch_y]
                elif not self.angle_selected:
                    self.angle_value = self.angle
                    self.angle_selected = True
                elif not self.power_selected:
                    self.power = (self.power_cursor_y - self.power_bar_y) / self.power_bar_height
                    self.v0 = self.throw_power * (1 - self.power)  # Adjust the launch speed
                    self.power_selected = True
                    self.vx = self.v0 * math.cos(self.angle_value)
                    self.vy = -self.v0 * math.sin(self.angle_value)
                
            elif event.key == pygame.K_r:
                self.reset_game()

    def update(self, dt):
        self.draw_background()
        pygame.draw.circle(self.screen, (0, 0, 0), (400, int(self.launch_y)), 5)

        if self.game_started and not self.angle_selected:
            self.draw_angle_arc()
            self.angle += self.angle_speed
            if self.angle > self.angle_max or self.angle < self.angle_min:
                self.angle_speed *= -1

        elif self.angle_selected and not self.power_selected:
            self.draw_power_bar()
            self.power_cursor_y += self.power_direction * self.power_speed
            if self.power_cursor_y < self.power_bar_y or self.power_cursor_y > self.power_bar_y + self.power_bar_height - 10:
                self.power_direction *= -1
            self.power = (self.power_cursor_y - self.power_bar_y) / self.power_bar_height
            self.v0 = self.throw_power * (1 - self.power)
            self.draw_trajectory()

        elif self.power_selected:
            if self.projectile_position is not None:
                self.vy += self.gravity * dt
                self.projectile_position[0] += self.vx * dt
                self.projectile_position[1] += self.vy * dt
                pygame.draw.circle(self.screen, (200, 0, 0), (int(self.projectile_position[0]), int(self.projectile_position[1])), 5)

                if self.projectile_position[1] >= self.ground_level:
                    self.projectile_position[1] = self.ground_level
                    self.impact_position = self.projectile_position[:]
                    self.landing_distance = self.impact_position[0] - self.launch_x  # in pixels
                    self.projectile_position = None


            elif self.impact_position is not None:
                pygame.draw.circle(self.screen, (200, 0, 0), (int(self.impact_position[0]), int(self.impact_position[1])), 5)

                # Convert landing distance from pixels to meters
                landing_distance_in_meters = self.landing_distance / 50  # 1 meter = 50 pixels

                # Display landing distance in meters
                text = self.font.render(f"Distance: {landing_distance_in_meters:.2f} meters", True, (0, 0, 0))
                self.screen.blit(text, (-100 + self.screen.get_width() // 2, -100 + self.screen.get_height() // 2))

                # Message to restart
                restart_text = self.font.render("Press R to restart", True, (0, 0, 0))
                self.screen.blit(restart_text, (-100 + self.screen.get_width() // 2, self.screen.get_height() // 2))

def start_fishing_game():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Create the FishingGame object
    fishing_game = FishingGame(screen, font)

    # Run the fishing mini-game
    while True:
        dt = clock.tick(120) / 1000  # Time step

        screen.fill((255, 255, 255))  # White background

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            fishing_game.handle_input(event)

        # Update and render the fishing game
        fishing_game.update(dt)

        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
        screen.blit(fps_text, (1000, 1000))

        pygame.display.flip()

if __name__ == "__main__":
    start_fishing_game()