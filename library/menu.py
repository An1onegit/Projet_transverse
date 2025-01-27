import pygame

def MainMenu():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont('Calibri', 100)
    font = pygame.font.SysFont('Calibri', 50)

    title = title_font.render("Bear's fishing Empire", True, "BLACK")
    play_btn = pygame.Rect(810,500,300,60)
    play_txt = font.render("Play", True, (247, 135, 100))
    settings_btn = pygame.Rect(810,570,300,60)
    settings_txt = font.render("Settings", True, (247, 135, 100))
    quit_btn = pygame.Rect(810,640,300,60)
    quit_txt = font.render("Quit", True, (247, 135, 100))


    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return True
                if settings_btn.collidepoint(event.pos):
                    pass
                if quit_btn.collidepoint(event.pos):
                    running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((184, 111, 82))

        # RENDER YOUR GAME HERE
        screen.blit(title, (600,150))
        pygame.draw.rect(screen, (35, 28, 7), play_btn)
        pygame.draw.rect(screen, (35, 28, 7), settings_btn)
        pygame.draw.rect(screen, (35, 28, 7), quit_btn)
        screen.blit(play_txt, (play_btn.x,play_btn.y))
        screen.blit(settings_txt, (settings_btn.x,settings_btn.y))
        screen.blit(quit_txt, (quit_btn.x,quit_btn.y))

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


#MainMenu()