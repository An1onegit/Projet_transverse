import pygame
import math
import sys

# Initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# Game state
game_started = False
power_selected = False
angle_selected = False

# Launch power
power_bar_height = 200
power_bar_y = 200
power_cursor_y = power_bar_y
power_speed = 5
power_direction = 1

# Throw angle
angle = 0
angle_speed = 0.03
angle_max = math.pi / 2
angle_min = 0

# Throw data
power = 0
v0 = 0
angle_value = 0
projectile_position = None
impact_position = None
vx = 0
vy = 0
launch_y = 0
gravity = 9.81 * 50  # 50 pixels = 1 meter
landing_distance = None

ground_level = 500

def reset_game():
    global game_started, power_selected, angle_selected
    global power_cursor_y, power_direction, angle, angle_speed
    global power, v0, angle_value, projectile_position
    global impact_position, vx, vy, launch_y, landing_distance

    game_started = False
    power_selected = False
    angle_selected = False

    power_cursor_y = power_bar_y
    power_direction = 1
    angle = 0
    angle_speed = 0.03

    power = 0
    v0 = 0
    angle_value = 0
    projectile_position = None
    impact_position = None
    vx = 0
    vy = 0
    launch_y = ground_level - 10
    landing_distance = None

reset_game()

def draw_background():
    screen.fill(BLUE)
    pygame.draw.rect(screen, GREEN, (0, ground_level, 800, 100))

def draw_power_bar():
    pygame.draw.rect(screen, RED, (50, power_bar_y, 30, power_bar_height // 3))
    pygame.draw.rect(screen, YELLOW, (50, power_bar_y + power_bar_height // 3, 30, power_bar_height // 3))
    pygame.draw.rect(screen, GREEN, (50, power_bar_y + 2 * power_bar_height // 3, 30, power_bar_height // 3))
    pygame.draw.rect(screen, WHITE, (45, power_cursor_y, 40, 10))

def draw_angle_arc():
    pygame.draw.arc(screen, GRAY, (300, 350, 200, 100), math.pi - angle_max, math.pi - angle_min, 5)
    end_x = 400 + 100 * math.cos(math.pi - angle)
    end_y = 400 - 50 * math.sin(math.pi - angle)
    pygame.draw.line(screen, WHITE, (400, 400), (end_x, end_y), 4)

while True:
    dt = clock.tick(60) / 1000
    screen.fill(WHITE)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                elif not power_selected:
                    power = (power_cursor_y - power_bar_y) / power_bar_height
                    v0 = 600 * (1 - power)  # Adjust the launch speed
                    power_selected = True
                elif not angle_selected:
                    angle_value = angle
                    angle_selected = True
                    launch_y = ground_level - 10
                    projectile_position = [100, launch_y]
                    vx = v0 * math.cos(angle_value)
                    vy = -v0 * math.sin(angle_value)
            elif event.key == pygame.K_r:
                reset_game()

    # Power selection
    if game_started and not power_selected:
        draw_power_bar()
        power_cursor_y += power_direction * power_speed
        if power_cursor_y < power_bar_y or power_cursor_y > power_bar_y + power_bar_height - 10:
            power_direction *= -1

    # Angle selection
    elif power_selected and not angle_selected:
        draw_angle_arc()
        angle += angle_speed
        if angle > angle_max or angle < angle_min:
            angle_speed *= -1

    # Projectile motion
    elif angle_selected:
        if projectile_position is not None:
            vy += gravity * dt
            projectile_position[0] += vx * dt
            projectile_position[1] += vy * dt

            if projectile_position[1] >= ground_level:
                projectile_position[1] = ground_level
                impact_position = projectile_position[:]
                landing_distance = impact_position[0] - 100  # in pixels
                projectile_position = None

        if projectile_position is not None:
            pygame.draw.circle(screen, RED, (int(projectile_position[0]), int(projectile_position[1])), 5)
        elif impact_position is not None:
            pygame.draw.circle(screen, RED, (int(impact_position[0]), int(impact_position[1])), 5)
            
            # Convert landing distance from pixels to meters
            landing_distance_in_meters = landing_distance / 50  # 1 meter = 50 pixels

            # Display landing distance in meters
            text = font.render(f"Distance: {landing_distance_in_meters:.2f} meters", True, BLACK)
            screen.blit(text, (280, 100))

            # Message to restart
            restart_text = font.render("Press R to restart", True, BLACK)
            screen.blit(restart_text, (280, 140))

    pygame.display.flip()
