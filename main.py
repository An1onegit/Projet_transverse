import pygame
from library.utils import *
from library.fishing import FishingGame

def Main():
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Bear's Fishing Empire")

    # Load map and scale it
    tile_map = TileMap("sources/maps/mapTest2.tmx")
    map_surface = pygame.transform.scale_by(tile_map.surface, tile_map.zoom)

    sprite_group = CameraGroup(map_surface)
    tile_map.render_objects(sprite_group)
    interaction_zones = tile_map.load_interaction_zones()
    

    player = Player(pos=(3500, 3500), groups=sprite_group, hitboxes=tile_map.hitboxes)

    # Fishing mini-game setup
    font = pygame.font.SysFont(None, 36)
    text = font.render("Interact (E)", True, (255,255,255))
    fishing_game = FishingGame(screen, font)
    fishing_mode = False

    fps = 120
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(fps) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if fishing_mode:
                fishing_game.handle_input(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    fishing_mode = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    player.anim = 5

        interaction = player.check_interactions(interaction_zones)
   

        if fishing_mode:
            fishing_game.update(dt)
        else:
            screen.fill((134, 203, 146))
            sprite_group.update(dt)
            sprite_group.custom_draw(player)

            if interaction:
                # Show prompt text
                message_surface = font.render(interaction["message"], True, (255, 255, 255))
                screen.blit(message_surface, ((screen.get_width() // 2) - message_surface.get_width() // 2, screen.get_height() - 250))

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    if interaction["type"] == "fishing":
                        fishing_mode = True
                        fishing_game.reset_game()  
                    #elif interaction["type"] == "npc":
                    #    open_npc_dialog(interaction)  # Later: open a trade dialog

   
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    Main()