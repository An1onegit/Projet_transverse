#menu projet transverse

import pygame
from library.button import Button


def MainMenu():
    pygame. init()

    #creation of game window 
    SCREEN_WIDTH = 1442
    SCREEN_HEIGHT = 800

    #game variables
    game_paused = False

    screen = pygame. display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("main menu")

    #definition fonts 
    font = pygame.font.SysFont("Arial Black", 40)

    #define colors
    TEXT_COLOR = (255, 255, 255)

    #load images
    play_img = pygame.image.load("sources/img/bouton_PLAY.png").convert_alpha()
    quit_img = pygame.image.load("sources/img/bouton_QUIT.png").convert_alpha()
    settings_img = pygame.image.load("sources/img/bouton_SETTINGS.png").convert_alpha()
    tutorial_img = pygame.image.load("sources/img/bouton_TUTORIAL.png").convert_alpha()

    #create button instance
    play_button = Button(580, 350, play_img, 0.86)
    quit_button = Button(580, 450, quit_img, 0.86)
    settings_button = Button(580, 550, settings_img, 0.86)
    tutorial_button = Button(580, 650, tutorial_img, 0.86)



    def draw_text(text, font,text_col, x, y):
        image = font.render(text, True, text_col)
        screen.blit(image, (x,y))

    #game loop
    run = True 
    while run: 

        screen.fill((177,235,52))

        #checking if game is paused
        if game_paused == True: 
            if play_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            if settings_button.draw(screen):
                pass
            if tutorial_button.draw(screen):    
                pass
        else:
            draw_text("hey hey hey!", font, TEXT_COLOR, 600, 250)

        #event handler 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True

            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    MainMenu()