#menu projet transverse

import pygame
import button  

pygame.init()

# --- CONSTANTS ---
SCREEN_WIDTH = 1442
SCREEN_HEIGHT = 800
TEXT_COLOR = (255, 255, 255)
TITLE_TEXT_COLOR = (0, 0, 100) 

# --- GAME STATE ---
STATE_TITLE_SCREEN = 0
STATE_MAIN_MENU = 1
STATE_PLAYING = 2 # later
STATE_SETTINGS = 3 # later
STATE_TUTORIAL = 4 #later

# --- GAME INITIALIZATION ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("This Bear Is Fishing")

# fonts
font_menu = pygame.font.SysFont("Arial Black", 40)
font_title = pygame.font.SysFont("Arial", 50, bold=True)

# loading images
try:
    accueil_img = pygame.image.load("images_menu/proto_2_menu_projet_transverse.png").convert()
    #redimension of the background with respect to the screen size
    accueil_img = pygame.transform.scale(accueil_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    play_img = pygame.image.load("images_menu/bouton_PLAY.png").convert_alpha()
    quit_img = pygame.image.load("images_menu/bouton_QUIT.png").convert_alpha()
    settings_img = pygame.image.load("images_menu/bouton_SETTINGS.png").convert_alpha()
    tutorial_img = pygame.image.load("images_menu/bouton_TUTORIAL.png").convert_alpha()

except pygame.error as e:
    print(f"Erreur lors du chargement d'une image : {e}")
    print("Vérifie que les fichiers images existent et sont dans les bons dossiers.")
    pygame.quit()
    exit() 

# --- BUTTON INSTANCE ---
# positioning of the buttons

button_x = SCREEN_WIDTH // 2 - play_img.get_width() * 0.86 // 2
play_button = button.Button(button_x, 350, play_img, 0.86)
quit_button = button.Button(button_x, 450, quit_img, 0.86)
settings_button = button.Button(button_x, 550, settings_img, 0.86)
tutorial_button = button.Button(button_x, 650, tutorial_img, 0.86)

# --- Fonction Utile ---
def draw_text(text, font, text_col, x, y, center=False):
    img = font.render(text, True, text_col)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

# --- GAME VARIABLES ---
current_state = STATE_TITLE_SCREEN # écran titre 
run = True

# --- GAME LOOP ---
while run:

    # --- events holder ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # events to change state
        if current_state == STATE_TITLE_SCREEN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_state = STATE_MAIN_MENU 


    #screen by default
    screen.fill((177, 235, 52))

    if current_state == STATE_TITLE_SCREEN:
        screen.blit(accueil_img, (0, 0))

    elif current_state == STATE_MAIN_MENU:

        if play_button.draw(screen):
            print("Action: Jouer !") 
            # Ici, tu changeras l'état vers STATE_PLAYING quand ton jeu sera prêt
            # current_state = STATE_PLAYING
            # run = False # Ou quitter la boucle du menu pour lancer la boucle de jeu principale

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
print("Jeu quitté.")


if __name__ == "__main__":
    MainMenu()
