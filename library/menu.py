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

    menu_bg = pygame.image.load("sources/img/menu projet transverse.png").convert_alpha()
    menu_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))

    play_img = pygame.image.load("sources/img/bouton_PLAY.png").convert_alpha()
    settings_img = pygame.image.load("sources/img/bouton_SETTINGS.png").convert_alpha()
    settings_img = pygame.transform.scale(settings_img, (play_img.get_width(), play_img.get_height()))

    quit_img = pygame.image.load("sources/img/bouton_QUIT.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (play_img.get_width(), play_img.get_height()))
    #tutorial_img = pygame.image.load("sources/img/bouton_TUTORIAL.png").convert_alpha()

    # --- BUTTON INSTANCE ---
    # positioning of the buttons
    button_x = screen_width // 2 - play_img.get_width()
    play_button = Button(button_x, screen_height - (5/10) * screen_height, play_img, 2)
    settings_button = Button(button_x, screen_height - (4/10) * screen_height, settings_img, 2)
    quit_button = Button(button_x, screen_height - (3/10) * screen_height, quit_img, 2)
    #tutorial_button = Button(button_x, screen_height - 2/10*screen_height, tutorial_img, 2)

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
                    if event.key == pygame.K_ESCAPE:
                        run = False

        screen.fill((177, 235, 52))

        if current_state == STATE_TITLE_SCREEN:
            screen.blit(accueil_img, (0, 0))

        elif current_state == STATE_MAIN_MENU:
            screen.blit(menu_bg, (0, 0))    

            if play_button.draw(screen):
                mainGame()

            if quit_button.draw(screen):
                run = False 

            if settings_button.draw(screen):
                print("Action: Options !") 
                # current_state = STATE_SETTINGS 

            # if tutorial_button.draw(screen):
            #     print("Action: Tutoriel !") 
            #     # current_state = STATE_TUTORIAL # Pour plus tard

        pygame.display.update()

    pygame.quit()