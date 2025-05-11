import platform
import pygame
from library.utils import *
from library.fishing import FishingGame
from library.menu import Menu
from library.inventory import Inventory
from library.save_system import *
from library.introduction import play_cinematic, get_cinematic_scenes

def Main():
    pygame.init()

    # get the screen size depending on the user's plateform (Windows / Mac)
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    else:
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    
    pygame.display.set_caption("Bear's Fishing Empire")

    # cinematic if first time playing
    if not os.path.exists(SAVE_FILE_PATH):
        print("No save file found, playing cinematic.")
        cinematic_main_font_size = max(24, int(screen_height / 15))
        cinematic_prompt_font_size = max(18, int(screen_height / 40))
        
        cinematic_main_font = pygame.font.SysFont(None, cinematic_main_font_size)
        cinematic_prompt_font = pygame.font.SysFont(None, cinematic_prompt_font_size)

        actual_cinematic_scenes = get_cinematic_scenes()
        
        play_cinematic(screen, cinematic_main_font, cinematic_prompt_font, actual_cinematic_scenes)

    # load map and scale it
    tile_map = TileMap("sources/maps/FinalMap.tmx")
    map_surface = pygame.transform.scale_by(tile_map.surface, tile_map.zoom)

    sprite_group = CameraGroup(map_surface)
    tile_map.render_objects(sprite_group)
    interaction_zones = tile_map.load_interaction_zones()
    
    player = Player(pos=(1500, 1500), groups=sprite_group, hitboxes=tile_map.hitboxes)
    inventory = Inventory()
    sound_manager = SoundManager()

    # try to load game data
    loaded_game_state = load_game()

    if loaded_game_state:
        # Load player data
        player_state = loaded_game_state.get("player", get_default_player_data(player.position.x, player.position.y))
        player.position.x = player_state.get("pos_x", player.position.x)
        player.position.y = player_state.get("pos_y", player.position.y)

        player.hitbox.center = player.position
        player.rect.midbottom = player.hitbox.midbottom

        inventory_state = loaded_game_state.get("inventory", get_default_inventory_data())
        inventory.money = inventory_state.get("money", inventory.money)
        inventory.fishes = inventory_state.get("fishes", inventory.fishes)

        saved_rods = inventory_state.get("rods")
        if saved_rods is not None and isinstance(saved_rods, list) and len(saved_rods) > 0:
            inventory.rods = saved_rods
        elif not inventory.rods:
             inventory.rods = ["Basic Rod"]


        saved_equipped_rod = inventory_state.get("equipped_rod")
        if saved_equipped_rod is not None and saved_equipped_rod in inventory.rods:
            inventory.equipped_rod = saved_equipped_rod
        elif inventory.rods: 
            inventory.equipped_rod = inventory.rods[0]
        else:
            inventory.rods = ["Basic Rod"]
            inventory.equipped_rod = "Basic Rod"
            
        if inventory.equipped_rod not in inventory.rods:
            if inventory.rods:
                 inventory.equipped_rod = inventory.rods[0]
            else:
                 inventory.rods = ["Basic Rod"]
                 inventory.equipped_rod = "Basic Rod"

    # Fishing mini-game setup
    font = pygame.font.SysFont(None, 60)
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
        "Tiny Bass": 10,
        "Minnow": 15,
        "Bluegill": 16,
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

    ROD_IMAGES = {
        "Basic Rod": pygame.image.load("sources/img/rods/basic.png").convert_alpha(),
        "Advanced Rod": pygame.image.load("sources/img/rods/advanced.png").convert_alpha(),
        "Super Rod": pygame.image.load("sources/img/rods/super.png").convert_alpha(),
        "Legendary Rod": pygame.image.load("sources/img/rods/legendary.png").convert_alpha()
    }

    ROD_IMAGE_SIZE = (60, 60)
    for key in ROD_IMAGES:
        ROD_IMAGES[key] = pygame.transform.scale(ROD_IMAGES[key], ROD_IMAGE_SIZE)
    
    fishing_game = FishingGame(screen, font, inventory, FISH_IMAGES)
    fishing_mode = False
    inventory_open = False
    selling_open = False
    shopping_open = False

    ROD_SHOP = {
        rod: price for rod, price in zip(
            ["Advanced Rod", "Super Rod", "Legendary Rod"],
            [100, 300, 1000]
        )
    }

    fps = 120
    clock = pygame.time.Clock()

    sound_manager.play_music("forest", True, .4)

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
                    if event.key == pygame.K_DELETE:
                        running = False
                        player_data_to_save = {
                        "position": player.position
                        }
                        inventory_data_to_save = {
                            "money": inventory.money,
                            "fishes": inventory.fishes,
                            "rods": inventory.rods,
                            "equipped_rod": inventory.equipped_rod
                        }
                        save_game(player_data_to_save, inventory_data_to_save)
                        Menu(Main)
                    if event.key == pygame.K_m:
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
                        fish_rect = pygame.Rect(fish_x, fish_y, 300, 40)  

                        if fish_rect.collidepoint(pygame.mouse.get_pos()):
                            # Sell this fish
                            inventory.sell_fish(fish, FISH_PRICES[fish])
                            sound_manager.play_sfx("money")
                            break
                elif shopping_open:
                    for idx, rod_name in enumerate(ROD_SHOP):
                        rod_display_y = panel_y + 70 + idx * (ROD_IMAGE_SIZE[1] + 20)
                        clickable_width = ROD_IMAGE_SIZE[0] + 300
                        rod_rect = pygame.Rect(panel_x + 20, rod_display_y, clickable_width, ROD_IMAGE_SIZE[1])

                        if rod_rect.collidepoint(pygame.mouse.get_pos()):
                            if rod_name not in inventory.rods:
                                if inventory.buy_rod(rod_name, ROD_SHOP[rod_name]):
                                    sound_manager.play_sfx("money")
                            break
                elif inventory_open:
                    for idx, rod in enumerate(inventory.rods):
                        rod_display_y = rod_start_y + (idx + 1) * 50
                        
                        clickable_width = ROD_IMAGE_SIZE[0] + 300
                        rod_rect = pygame.Rect(panel_x + 20, rod_display_y, clickable_width, ROD_IMAGE_SIZE[1])
                        
                        if rod_rect.collidepoint(pygame.mouse.get_pos()):
                            inventory.equip_rod(rod)
                            break


        if fishing_mode:
            fishing_game.update(dt)
            screen.fill((134, 203, 146))  
            fishing_game.draw()
        else:
            screen.fill((134, 203, 146))
            sprite_group.update(dt)
            sprite_group.custom_draw(player)

            if inventory_open:
                # Inventory Panel
                panel_width = 800
                panel_height = 600
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

                for idx, rod_name in enumerate(inventory.rods):
                    is_equipped = rod_name == inventory.equipped_rod
                    color = (0, 255, 0) if is_equipped else (200, 200, 255)
                    
                    current_rod_y = rod_start_y + (idx + 1) * 50 # Increased spacing for image
                    
                    # Draw the rod image
                    if rod_name in ROD_IMAGES:
                        img = ROD_IMAGES[rod_name]
                        img_x = panel_x + 20
                        img_y = current_rod_y + (font.get_height() - img.get_height()) // 2 
                        screen.blit(img, (img_x, img_y))
                        text_offset_x = img.get_width() + 10
                    else:
                        text_offset_x = 0

                    rod_text_content = f"{rod_name}" + (" (Equipped)" if is_equipped else "")
                    rod_text = font.render(rod_text_content, True, color)
                    screen.blit(rod_text, (panel_x + 20 + text_offset_x, current_rod_y))

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
                for idx, rod_name in enumerate(ROD_SHOP):
                    current_rod_y = fishing_rod_start_y + idx * (ROD_IMAGE_SIZE[1] + 20)
                    
                    img_x = panel_x + 20
                    text_offset_x = 0

                    # Draw the rod image
                    if rod_name in ROD_IMAGES:
                        img = ROD_IMAGES[rod_name]
                        img_y = current_rod_y + (font.get_height() - img.get_height()) // 2
                        screen.blit(img, (img_x, img_y))
                        text_offset_x = img.get_width() + 10
                    
                    rod_display_text = ""
                    text_color = (255,255,255)

                    if rod_name in inventory.rods:
                        rod_display_text = f"{rod_name} - OWNED"
                        text_color = (100, 100, 100)
                    else:
                        if inventory.money >= ROD_SHOP[rod_name]:
                            rod_display_text = f"{rod_name} - ${ROD_SHOP[rod_name]}"
                            text_color = (100, 255, 100)
                        else:
                            rod_display_text = f"{rod_name} - ${ROD_SHOP[rod_name]}"
                            text_color = (255, 100, 100)
                    
                    rod_text_surface = font.render(rod_display_text, True, text_color)
                    screen.blit(rod_text_surface, (img_x + text_offset_x, current_rod_y))

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

    player_data_to_save = {
        "position": player.position
    }
    inventory_data_to_save = {
        "money": inventory.money,
        "fishes": inventory.fishes,
        "rods": inventory.rods,
        "equipped_rod": inventory.equipped_rod
    }
    save_game(player_data_to_save, inventory_data_to_save)
    pygame.quit()

if __name__ == "__main__":
    Menu(Main)