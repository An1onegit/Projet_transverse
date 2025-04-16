import pygame

def start_menu(next_screen):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("This Bear is Fishing!")
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    background = pygame.image.load("sources/img/proto_2_menu_projet_transverse.png")
    background = pygame.transform.scale_by(background, .78)
    
    running = True
    while running:
        screen.fill((0,0,0))
        #text = font.render("Press SPACE to Start", True, (255, 255, 255))
        #screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height() - 250))


        screen.blit(background, (220,100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

        clock.tick(120)
        
        pygame.display.flip()

    next_screen()


if __name__ == "__main__":
    start_menu(start_menu)