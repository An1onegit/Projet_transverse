import pygame
import math
import sys

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# État du jeu
game_started = False
power_selected = False
angle_selected = False

# Jauge de puissance
power_bar_height = 200
power_bar_y = 200
power_cursor_y = power_bar_y
power_speed = 5
power_direction = 1

# Jauge d'angle
angle = 0
angle_speed = 0.03
angle_max = math.pi / 3
angle_min = -math.pi / 3

# Données du tir
power = 0
projectile_position = None
time_elapsed = 0
v0 = 0
angle_value = 0

# Lieux
ground_level = 500

def draw_background():
    screen.fill(BLUE)
    pygame.draw.rect(screen, GREEN, (0, ground_level, 800, 100))

def draw_power_bar():
    # Fond
    pygame.draw.rect(screen, RED, (50, power_bar_y, 30, power_bar_height // 3))
    pygame.draw.rect(screen, YELLOW, (50, power_bar_y + power_bar_height // 3, 30, power_bar_height // 3))
    pygame.draw.rect(screen, GREEN, (50, power_bar_y + 2 * power_bar_height // 3, 30, power_bar_height // 3))
    # Curseur
    pygame.draw.rect(screen, WHITE, (45, power_cursor_y, 40, 10))

def draw_angle_arc():
    pygame.draw.arc(screen, GRAY, (300, 350, 200, 100), math.pi - angle_max, math.pi - angle_min, 5)
    # Curseur de direction
    end_x = 400 + 100 * math.cos(math.pi - angle)
    end_y = 400 - 50 * math.sin(math.pi - angle)
    pygame.draw.line(screen, WHITE, (400, 400), (end_x, end_y), 4)

def launch_projectile(v0, angle):
    global time_elapsed
    t = time_elapsed
    x = 100 + v0 * math.cos(angle) * t
    y = ground_level - (v0 * math.sin(angle) * t - 0.5 * 9.81 * t ** 2)
    return (x, y)

# Boucle principale
while True:
    dt = clock.tick(60) / 1000
    screen.fill(WHITE)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_started:
                game_started = True
            elif not power_selected:
                power = (power_cursor_y - power_bar_y) / power_bar_height
                v0 = 100 * (1 - power)  # plus haut = plus rapide
                power_selected = True
            elif not angle_selected:
                angle_value = angle
                angle_selected = True
                projectile_position = (100, ground_level)
                time_elapsed = 0

    if game_started and not power_selected:
        draw_power_bar()
        power_cursor_y += power_direction * power_speed
        if power_cursor_y < power_bar_y or power_cursor_y > power_bar_y + power_bar_height - 10:
            power_direction *= -1
    elif power_selected and not angle_selected:
        draw_angle_arc()
        angle += angle_speed
        if angle > angle_max or angle < angle_min:
            angle_speed *= -1
    elif angle_selected:
        time_elapsed += dt
        pos = launch_projectile(v0, angle_value)
        if pos[1] < ground_level:
            pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), 5)
        else:
            pygame.draw.circle(screen, RED, (int(pos[0]), int(ground_level)), 5)

    pygame.display.flip()
