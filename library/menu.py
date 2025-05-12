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
    STATE_PLAYING = 2
    STATE_SETTINGS = 3
    STATE_TUTORIAL = 4

    # --- INITIALIZATION ---
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("This Bear Is Fishing")

    accueil_img = pygame.image.load("sources/img/proto_2_menu_projet_transverse.png").convert()
    accueil_img = pygame.transform.scale(accueil_img, (screen_width, screen_height))

    menu_bg = pygame.image.load("sources/img/menu projet transverse.png").convert_alpha()
    menu_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))

    play_img = pygame.image.load("sources/img/bouton_PLAY.png").convert_alpha()
    settings_img = pygame.image.load("sources/img/bouton_SETTINGS.png").convert_alpha()
    settings_img = pygame.transform.scale(settings_img, (play_img.get_width(), play_img.get_height()))
    quit_img = pygame.image.load("sources/img/bouton_QUIT.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (play_img.get_width(), play_img.get_height()))

    button_x = screen_width // 2 - play_img.get_width()
    play_button = Button(button_x, screen_height - (5/10) * screen_height, play_img, 2)
    settings_button = Button(button_x, screen_height - (4/10) * screen_height, settings_img, 2)
    quit_button = Button(button_x, screen_height - (3/10) * screen_height, quit_img, 2)

    show_settings = False
    fullscreen = True
    volume = 5  # from 0 to 10

    font = pygame.font.SysFont("Arial", 40)

    def draw_settings_panel():
        panel_width = screen_width // 2
        panel_height = screen_height // 2
        panel_x = screen_width // 2 - panel_width // 2
        panel_y = screen_height // 2 - panel_height // 2

        # Shadow
        shadow_rect = pygame.Surface((panel_width + 10, panel_height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow_rect, (0, 0, 0, 120), shadow_rect.get_rect(), border_radius=20)
        screen.blit(shadow_rect, (panel_x - 5, panel_y - 5))

        # Panel background (translucent and rounded)
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (20, 20, 30, 230), (0, 0, panel_width, panel_height), border_radius=20)
        screen.blit(panel_surf, (panel_x, panel_y))

        # Title
        title = font.render("⚙️ Settings", True, (255, 255, 255))
        screen.blit(title, (panel_x + 30, panel_y + 30))

        # Volume bar
        vol_label = font.render("Volume", True, (220, 220, 220))
        screen.blit(vol_label, (panel_x + 30, panel_y + 120))

        # Draw volume bar
        vol_bar_x = panel_x + 200
        vol_bar_y = panel_y + 130
        vol_bar_width = 200
        vol_bar_height = 20
        pygame.draw.rect(screen, (80, 80, 80), (vol_bar_x, vol_bar_y, vol_bar_width, vol_bar_height), border_radius=10)
        pygame.draw.rect(screen, (0, 180, 255), (vol_bar_x, vol_bar_y, (volume / 10) * vol_bar_width, vol_bar_height), border_radius=10)

        # Fullscreen toggle
        fs_label = font.render("Fullscreen", True, (220, 220, 220))
        screen.blit(fs_label, (panel_x + 30, panel_y + 200))
        fs_state = font.render("ON" if fullscreen else "OFF", True, (0, 255, 0) if fullscreen else (255, 50, 50))
        screen.blit(fs_state, (panel_x + 250, panel_y + 200))

        # Footer
        tip_text = pygame.font.SysFont("Arial", 25).render("← → to adjust volume | F to toggle fullscreen | ESC to close", True, (160, 160, 160))
        screen.blit(tip_text, (panel_x + 30, panel_y + panel_height - 50))


    current_state = STATE_TITLE_SCREEN
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if show_settings:
                        show_settings = False
                    else:
                        run = False

                if show_settings:
                    if event.key == pygame.K_RIGHT:
                        volume = min(10, volume + 1)
                    elif event.key == pygame.K_LEFT:
                        volume = max(0, volume - 1)
                    elif event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        screen = pygame.display.set_mode(
                            (screen_width, screen_height), 
                            pygame.FULLSCREEN if fullscreen else 0
                        )

                elif current_state == STATE_TITLE_SCREEN and event.key == pygame.K_SPACE:
                    current_state = STATE_MAIN_MENU

                elif current_state == STATE_MAIN_MENU and event.key == pygame.K_SPACE:
                    mainGame()

        screen.fill((0, 0, 0))

        if current_state == STATE_TITLE_SCREEN:
            screen.blit(accueil_img, (0, 0))

        elif current_state == STATE_MAIN_MENU:
            screen.blit(menu_bg, (0, 0))

            if play_button.draw(screen):
                mainGame()

            if settings_button.draw(screen):
                show_settings = not show_settings

            if quit_button.draw(screen):
                run = False

        if show_settings:
            draw_settings_panel()

        pygame.display.update()

    pygame.quit()
