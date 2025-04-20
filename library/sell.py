import pygame

def SellMenu():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Calibri', 80)

    title = font.render("Fish Market - Sell Your Fish", True, "BLACK")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((255, 230, 200))  # soft orange background

        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 150))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
