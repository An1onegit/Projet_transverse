import platform
import pygame
from library.utils import *

def Menu(mainGame):
    pygame.init()
    
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    else:
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h


    # --- GAME STATE ---
    STATE_TITLE_SCREEN = 0
    STATE_MAIN_MENU = 1
    STATE_PLAYING = 2 # later
    STATE_SETTINGS = 3 # later
    STATE_TUTORIAL = 4 #later

    # --- GAME INITIALIZATION ---
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("This Bear Is Fishing")

    # loading images
    accueil_img = pygame.image.load("sources/img/proto_2_menu_projet_transverse.png").convert()
    accueil_img = pygame.transform.scale(accueil_img, (screen_width, screen_height))

    play_img = pygame.image.load("sources/img/bouton_PLAY.png").convert_alpha()
    quit_img = pygame.image.load("sources/img/bouton_QUIT.png").convert_alpha()
    settings_img = pygame.image.load("sources/img/bouton_SETTINGS.png").convert_alpha()
    tutorial_img = pygame.image.load("sources/img/bouton_TUTORIAL.png").convert_alpha()

    # --- BUTTON INSTANCE ---
    # positioning of the buttons
    button_x = screen_width // 2 - play_img.get_width() // 2
    play_button = Button(button_x, 350, play_img, 1)
    quit_button = Button(button_x, 450, quit_img, 1)
    settings_button = Button(button_x, 550, settings_img, 1)
    tutorial_button = Button(button_x, 650, tutorial_img, 1)

    current_state = STATE_TITLE_SCREEN

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if current_state == STATE_TITLE_SCREEN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_state = STATE_MAIN_MENU 
            elif current_state == STATE_MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        mainGame()

        screen.fill((177, 235, 52))

        if current_state == STATE_TITLE_SCREEN:
            screen.blit(accueil_img, (0, 0))

        elif current_state == STATE_MAIN_MENU:

            if play_button.draw(screen):
                mainGame()

            if quit_button.draw(screen):
                run = False 

            if settings_button.draw(screen):
                print("Action: Options !") 
                # current_state = STATE_SETTINGS 

            if tutorial_button.draw(screen):
                print("Action: Tutoriel !") 
                # current_state = STATE_TUTORIAL # Pour plus tard

        pygame.display.update()

    pygame.quit()