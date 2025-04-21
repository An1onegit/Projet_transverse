import pygame
from library.utils import *
from library.fishing import FishingGame
from library.preMenu import start_menu
from library.menu import MainMenu
from library.inventory import Inventory

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
    
    player = Player(pos=(4500, 4500), groups=sprite_group, hitboxes=tile_map.hitboxes)
    inventory = Inventory()

    # Fishing mini-game setup
    font = pygame.font.SysFont(None, 36)
    FISH_IMAGES = {
        "Small Carp": pygame.image.load("sources/img/fishes/tile000.png").convert_alpha(),
        "Tiny Bass": pygame.image.load("sources/img/fishes/tile001.png").convert_alpha(),
        "Minnow": pygame.image.load("sources/img/fishes/tile002.png").convert_alpha(),
        "Bluegill": pygame.image.load("sources/img/fishes/tile003.png").convert_alpha(),
        "Pike": pygame.image.load("sources/img/fishes/tile004.png").convert_alpha(),
        "Perch": pygame.image.load("sources/img/fishes/tile005.png").convert_alpha(),
        "Golden Trout": pygame.image.load("sources/img/fishes/tile006.png").convert_alpha(),
        "Catfish": pygame.image.load("sources/img/fishes/tile007.png").convert_alpha(),
        "Silver Salmon": pygame.image.load("sources/img/fishes/tile008.png").convert_alpha(),
        "Giant Tuna": pygame.image.load("sources/img/fishes/tile009.png").convert_alpha(),
        "Swordfish": pygame.image.load("sources/img/fishes/tile010.png").convert_alpha(),
        "Mahi-Mahi": pygame.image.load("sources/img/fishes/tile011.png").convert_alpha(),
        "Ancient Coelacanth": pygame.image.load("sources/img/fishes/tile012.png").convert_alpha(),
        "Mythical Leviathan": pygame.image.load("sources/img/fishes/tile013.png").convert_alpha(),
        "Rainbow Koi": pygame.image.load("sources/img/fishes/tile014.png").convert_alpha()
    }

    for key in FISH_IMAGES:
        FISH_IMAGES[key] = pygame.transform.scale(FISH_IMAGES[key], (40, 40))
    FISH_PRICES = {
        "Small Carp": 5,
        "Tiny Bass": 7,
        "Minnow": 10,
        "Bluegill": 15,
        "Pike": 20,
        "Perch": 25,
        "Golden Trout": 40,
        "Catfish": 50,
        "Silver Salmon": 60,
        "Giant Tuna": 80,
        "Swordfish": 100,
        "Mahi-Mahi": 120,
        "Ancient Coelacanth": 200,
        "Mythical Leviathan": 500,
        "Rainbow Koi": 1000
    }

    fishing_game = FishingGame(screen, font, inventory, FISH_IMAGES)
    fishing_mode = False
    inventory_open = False
    selling_open = False
    shopping_open = False

    ROD_SHOP = {
        "Advanced Rod":100,
        "Super Rod": 300,
        "Legendary Rod": 1000
    }

    fps = 120
    clock = pygame.time.Clock()

    running = True
    while running:
        interaction = player.check_interactions(interaction_zones)

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
                    if event.key == pygame.K_i:
                        inventory_open = not inventory_open
                    if event.key == pygame.K_e:
                        if interaction:
                            if interaction["type"] == "sell":
                                selling_open = not selling_open
                                inventory_open = False
                            elif interaction["type"] == "fishing":
                                fishing_mode = True
                                fishing_game.reset_game()
                            elif interaction["type"] == "shop":
                                shopping_open = not shopping_open
                                inventory_open = False
                else:
                    player.anim = 5
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selling_open:
                    for idx, fish in enumerate(inventory.fishes):
                        fish_x = panel_x + 20
                        fish_y = panel_y + 70 + idx * 50
                        fish_rect = pygame.Rect(fish_x, fish_y, 300, 40)  # area for each fish

                        if fish_rect.collidepoint(pygame.mouse.get_pos()):
                            # Sell this fish
                            inventory.sell_fish(fish, FISH_PRICES[fish])
                            break
                elif shopping_open:
                    for idx, rod in enumerate(ROD_SHOP):
                        rod_x = panel_x + 20
                        rod_y = panel_y + 70 + idx * 50
                        rod_rect = pygame.Rect(rod_x, rod_y, 300, 40)  # area for each fish

                        if rod_rect.collidepoint(pygame.mouse.get_pos()):
                            if rod not in inventory.rods:
                                # Sell this fish
                                inventory.buy_rod(rod, ROD_SHOP[rod])
                            break

        if fishing_mode:
            fishing_game.update(dt)
            screen.fill((134, 203, 146))  # Background color during fishing
            fishing_game.draw()          # Draw the fishing mini-game
        else:
            screen.fill((134, 203, 146))
            sprite_group.update(dt)
            sprite_group.custom_draw(player)

            if inventory_open:
                # Inventory Panel
                panel_width = 500
                panel_height = 400
                panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                panel_surface.fill((50, 50, 50, 220))
                panel_x = (screen.get_width() - panel_width) // 2
                panel_y = (screen.get_height() - panel_height) // 2
                screen.blit(panel_surface, (panel_x, panel_y))

                # Money
                money_text = font.render(f"Money: ${inventory.money}", True, (255, 255, 0))
                screen.blit(money_text, (panel_x + panel_width - money_text.get_width() - 20, panel_y + 20))

                # Fishes
                fish_start_y = panel_y + 70
                for idx, fish in enumerate(inventory.fishes):
                    # Draw the fish image
                    if fish in FISH_IMAGES:
                        img = FISH_IMAGES[fish]
                        img_x = panel_x + 20
                        img_y = fish_start_y + idx * 50
                        screen.blit(img, (img_x, img_y))

                    # Draw the fish name next to it
                    fish_text = font.render(fish, True, (255, 255, 255))
                    screen.blit(fish_text, (img_x + 50, img_y + 10))  # 10px vertical adjust


                # Rods
                rod_start_y = fish_start_y + len(inventory.fishes) * 40 + 30
                rod_title = font.render("Rods:", True, (255, 255, 255))
                screen.blit(rod_title, (panel_x + 20, rod_start_y))
                for idx, rod in enumerate(inventory.rods):
                    rod_text = font.render(f"{rod}", True, (200, 200, 255))
                    screen.blit(rod_text, (panel_x + 20, rod_start_y + (idx + 1) * 30))

            if selling_open:
                # Sell Panel
                panel_width = 800
                panel_height = 600
                panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                panel_surface.fill((50, 50, 50, 220))
                panel_x = (screen.get_width() - panel_width) // 2
                panel_y = (screen.get_height() - panel_height) // 2
                screen.blit(panel_surface, (panel_x, panel_y))

                # Title
                sell_title = font.render("Sell your fish", True, (255, 255, 255))
                screen.blit(sell_title, (panel_x + 20, panel_y + 20))

                # Money
                money_text = font.render(f"Money: ${inventory.money}", True, (255, 255, 0))
                screen.blit(money_text, (panel_x + panel_width - money_text.get_width() - 20, panel_y + 20))

                # Fishes for sale
                fish_start_y = panel_y + 70
                for idx, fish in enumerate(inventory.fishes):
                    if fish in FISH_IMAGES:
                        img = FISH_IMAGES[fish]
                        img_x = panel_x + 20
                        img_y = fish_start_y + idx * 50
                        screen.blit(img, (img_x, img_y))

                    fish_text = font.render(f"{fish} - ${FISH_PRICES[fish]}", True, (255, 255, 255))
                    screen.blit(fish_text, (img_x + 50, img_y + 10))

                # Instructions
                info_text = font.render("Click a fish to sell it!", True, (255, 255, 0))
                screen.blit(info_text, (panel_x + panel_width // 2 - info_text.get_width() // 2, panel_y + panel_height - 40))

            if shopping_open:
                # Shop Panel
                panel_width = 800
                panel_height = 600
                panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                panel_surface.fill((50, 50, 50, 220))
                panel_x = (screen.get_width() - panel_width) // 2
                panel_y = (screen.get_height() - panel_height) // 2
                screen.blit(panel_surface, (panel_x, panel_y))

                # Title
                sell_title = font.render("Buy a new fishing rod !", True, (255, 255, 255))
                screen.blit(sell_title, (panel_x + 20, panel_y + 20))

                # Money
                money_text = font.render(f"Money: ${inventory.money}", True, (255, 255, 0))
                screen.blit(money_text, (panel_x + panel_width - money_text.get_width() - 20, panel_y + 20))

                fishing_rod_start_y = panel_y + 70
                for idx, rod in enumerate(ROD_SHOP):
                    img_x = panel_x + 20
                    img_y = fishing_rod_start_y + idx * 50
                    if rod in inventory.rods:
                        rod_text = font.render(f"{rod} - OWNED", True, (100, 100, 100))
                    else:
                        if inventory.money >= ROD_SHOP[rod]:
                            rod_text = font.render(f"{rod} - ${ROD_SHOP[rod]}", True, (100, 255, 100))
                        else:
                            rod_text = font.render(f"{rod} - ${ROD_SHOP[rod]}", True, (255, 100, 100))
                    screen.blit(rod_text, (img_x + 50, img_y + 10))

                # Instructions
                info_text = font.render("Click a fishing rod to buy it!", True, (255, 255, 0))
                screen.blit(info_text, (panel_x + panel_width // 2 - info_text.get_width() // 2, panel_y + panel_height - 40))

            if interaction:
                message_surface = font.render(interaction["message"], True, (255, 255, 255))
                screen.blit(message_surface, ((screen.get_width() - message_surface.get_width()) // 2, screen.get_height() - 200))
            else:
                selling_open = False 
                shopping_open = False
                    

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    #start_menu(lambda: MainMenu(Main))
    Main()