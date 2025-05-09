import pygame

def get_cinematic_scenes():
    return [
        {
            "image_path": "sources/img/introduction/storm.png",
            "text": "In the heart of a whispering forest, where ancient trees touched the sky and rivers sang forgotten songs, lived a bear unlike any other."
        },
        {
            "image_path": "sources/img/introduction/storm.png", 
            "text": "This bear, known to the rustling leaves and babbling brooks as Barnaby, wasn't content with just berries and naps. He had a peculiar glint in his eye, a yearning for something more..."
        },
        {
            "image_path": "sources/img/introduction/storm.png",
            "text": "One day, watching a glint of silver in the water, Barnaby discovered the thrill of fishing! It wasn't just food; it was an art, a challenge, a passion."
        },
        {
            "image_path": "sources/img/introduction/storm.png",
            "text": "And so, 'This Bear is Fishing' began his journey, dreaming of becoming the greatest angler the forest had ever seen, building a true Fishing Empire from a humble pawful of fish."
        },
    ]

# function from https://www.pygame.org/wiki/TextWrap
def render_text_wrapped(surface, text, font, color, rect_area, aa=True, bkg=None):
    rect = pygame.Rect(rect_area)
    y = rect.top
    line_spacing = -2
    font_height = font.size("Tg")[1]
    while text:
        i = 1
        if y + font_height > rect.bottom: break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text):
            prev_space = text.rfind(" ", 0, i)
            if prev_space != -1: i = prev_space + 1
        try:
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left, y))
        except pygame.error as e:
            print(f"Error rendering text: {e}"); break
        y += font_height + line_spacing
        text = text[i:]
    return y


def play_cinematic(screen, main_font, prompt_font, scenes_data):
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()

    # --- Animation States ---
    STATE_SCENE_FADE_IN = 0
    STATE_IMAGE_FADE_IN = 1
    STATE_TEXT_TYPING = 2
    STATE_WAITING_INPUT = 3
    STATE_SCENE_FADE_OUT = 4
    STATE_FINISH_TYPING_QUICKLY = 5

    # --- Timings (milliseconds) ---
    SCENE_FADE_DURATION = 700
    IMAGE_FADE_DURATION = 1000
    TEXT_BOX_FADE_DURATION = 500 
    TYPING_CHAR_DELAY = 25

    # --- Text Box Setup ---
    text_box_height = screen_height // 3
    text_box_padding = 20
    text_box_rect = pygame.Rect(
        text_box_padding,
        screen_height - text_box_height - text_box_padding,
        screen_width - (2 * text_box_padding),
        text_box_height
    )
    text_area_rect = pygame.Rect(
        text_box_rect.left + text_box_padding,
        text_box_rect.top + text_box_padding,
        text_box_rect.width - (2 * text_box_padding),
        text_box_rect.height - (2 * text_box_padding)
    )
    text_box_bg_color_base = (20, 20, 20) 
    text_box_alpha_target = 200 

    # --- Full Screen Fade Overlay ---
    scene_fade_overlay = pygame.Surface((screen_width, screen_height))
    scene_fade_overlay.fill((0, 0, 0))

    for scene_index, current_scene_data in enumerate(scenes_data):
        current_state = STATE_SCENE_FADE_IN
        animation_start_time = pygame.time.get_ticks()
        
        scene_image = None
        img_rect = None
        if current_scene_data.get("image_path"):
            try:
                scene_image = pygame.image.load(current_scene_data["image_path"]).convert_alpha()
                img_aspect_ratio = scene_image.get_width() / scene_image.get_height()
                scaled_width = screen_width
                scaled_height = int(scaled_width / img_aspect_ratio)
                if scaled_height > screen_height:
                    scaled_height = screen_height
                    scaled_width = int(scaled_height * img_aspect_ratio)
                scene_image = pygame.transform.smoothscale(scene_image, (scaled_width, scaled_height))
                img_rect = scene_image.get_rect(center=(screen_width // 2, screen_height // 2))
            except pygame.error as e:
                print(f"Error loading cinematic image {current_scene_data['image_path']}: {e}")
                scene_image = None

        full_text = current_scene_data["text"]
        displayed_text = ""
        current_char_index = 0
        last_char_typed_time = 0

        current_scene_fade_alpha = 255
        current_image_alpha = 0
        current_text_box_alpha = 0


        scene_active = True
        while scene_active:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        pygame.mouse.set_visible(True)
                        return
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if current_state == STATE_SCENE_FADE_IN:
                            current_scene_fade_alpha = 0
                            animation_start_time = current_time
                            current_state = STATE_IMAGE_FADE_IN if scene_image else STATE_TEXT_TYPING
                        elif current_state == STATE_IMAGE_FADE_IN:
                            current_image_alpha = 255
                            current_text_box_alpha = text_box_alpha_target
                            animation_start_time = current_time
                            current_state = STATE_TEXT_TYPING
                            last_char_typed_time = current_time
                        elif current_state == STATE_TEXT_TYPING:
                            current_state = STATE_FINISH_TYPING_QUICKLY
                        elif current_state == STATE_WAITING_INPUT:
                            animation_start_time = current_time
                            current_state = STATE_SCENE_FADE_OUT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if current_state == STATE_SCENE_FADE_IN:
                        current_scene_fade_alpha = 0
                        animation_start_time = current_time
                        current_state = STATE_IMAGE_FADE_IN if scene_image else STATE_TEXT_TYPING
                    elif current_state == STATE_IMAGE_FADE_IN:
                        current_image_alpha = 255
                        current_text_box_alpha = text_box_alpha_target
                        animation_start_time = current_time
                        current_state = STATE_TEXT_TYPING
                        last_char_typed_time = current_time
                    elif current_state == STATE_TEXT_TYPING:
                        current_state = STATE_FINISH_TYPING_QUICKLY
                    elif current_state == STATE_WAITING_INPUT:
                        animation_start_time = current_time
                        current_state = STATE_SCENE_FADE_OUT
            
            elapsed_time = current_time - animation_start_time

            if current_state == STATE_SCENE_FADE_IN:
                progress = min(elapsed_time / SCENE_FADE_DURATION, 1.0)
                current_scene_fade_alpha = int(255 * (1 - progress))
                if progress >= 1.0:
                    animation_start_time = current_time
                    current_state = STATE_IMAGE_FADE_IN if scene_image else STATE_TEXT_TYPING
                    if not scene_image: last_char_typed_time = current_time


            elif current_state == STATE_IMAGE_FADE_IN:
                img_progress = min(elapsed_time / IMAGE_FADE_DURATION, 1.0)
                current_image_alpha = int(255 * img_progress)

                txt_box_progress = min(elapsed_time / TEXT_BOX_FADE_DURATION, 1.0)
                current_text_box_alpha = int(text_box_alpha_target * txt_box_progress)

                if img_progress >= 1.0:
                    current_image_alpha = 255
                    current_text_box_alpha = text_box_alpha_target
                    animation_start_time = current_time
                    current_state = STATE_TEXT_TYPING
                    last_char_typed_time = current_time

            elif current_state == STATE_TEXT_TYPING:
                if current_char_index < len(full_text):
                    if current_time - last_char_typed_time >= TYPING_CHAR_DELAY:
                        displayed_text += full_text[current_char_index]
                        current_char_index += 1
                        last_char_typed_time = current_time
                else:
                    animation_start_time = current_time
                    current_state = STATE_WAITING_INPUT
            
            elif current_state == STATE_FINISH_TYPING_QUICKLY:
                displayed_text = full_text
                current_char_index = len(full_text)
                current_state = STATE_WAITING_INPUT

            elif current_state == STATE_WAITING_INPUT:
                pass

            elif current_state == STATE_SCENE_FADE_OUT:
                progress = min(elapsed_time / SCENE_FADE_DURATION, 1.0)
                current_scene_fade_alpha = int(255 * progress)
                if progress >= 1.0:
                    scene_active = False

            # --- Drawing ---
            screen.fill((0, 0, 0))

            if current_image_alpha > 0:
                scene_image.set_alpha(current_image_alpha)
                screen.blit(scene_image, img_rect)

            if current_text_box_alpha > 0:
                temp_text_box_surface = pygame.Surface((text_box_rect.width, text_box_rect.height), pygame.SRCALPHA)
                temp_text_box_surface.fill((*text_box_bg_color_base, current_text_box_alpha))
                screen.blit(temp_text_box_surface, text_box_rect.topleft)

            if current_text_box_alpha > text_box_alpha_target * 0.5:
                text_color = (230, 230, 230)
                render_text_wrapped(screen, displayed_text, main_font, text_color, text_area_rect)

            if current_state == STATE_WAITING_INPUT:
                prompt_text = "Press [Enter] or Click to Continue... (Esc to Skip)"
                prompt_surface = prompt_font.render(prompt_text, True, (200, 200, 0))
                prompt_rect = prompt_surface.get_rect(centerx=screen_width // 2, y=screen_height - prompt_surface.get_height() - 10)
                screen.blit(prompt_surface, prompt_rect)
            
            if current_scene_fade_alpha > 0:
                scene_fade_overlay.set_alpha(current_scene_fade_alpha)
                screen.blit(scene_fade_overlay, (0,0))

            pygame.display.flip()

    pygame.mouse.set_visible(True)