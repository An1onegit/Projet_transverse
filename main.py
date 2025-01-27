# Example file showing a basic pygame "game loop"
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Bear's Fishing Empire")

clock = pygame.time.Clock()
running = True

fps = 60
clock = pygame.time.Clock()

# Player's caracteristics
## Coordinates 
x = 250
y = 250

##Size
width = 50
height = 50


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")
    
    keys = pygame.key.get_pressed()
    # Initialize movement variables
    x_change = 0
    y_change = 0

    # Handle key inputs
    if keys[pygame.K_d]:
        x_change += 5   
    if keys[pygame.K_q]:
        x_change -= 5
    if keys[pygame.K_s]:
        y_change += 5
    if keys[pygame.K_z]:
        y_change -= 5

    # Normalize diagonal movement
    if x_change != 0 and y_change != 0:
        # Divide each component by sqrt(2) to normalize the vector
        x_change /= math.sqrt(2)
        y_change /= math.sqrt(2)

    # Update the position
    x += x_change
    y += y_change

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen,(255,0,0),(x,y,width,height))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(fps)  # limits FPS to 60

pygame.quit()