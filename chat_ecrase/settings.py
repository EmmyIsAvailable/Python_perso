import pygame, functions, pickle

inactive_color = (0, 0, 0)
active_color = (50, 0, 0)
black = (0, 0, 0)

def sound_click():
    click_sound = pygame.mixer.Sound("sounds/click2.mp3")
    pygame.mixer.Sound.play(click_sound)

def affichage(screen_surface, text, x, y, w, h, color):
    pygame.draw.rect(screen_surface, color, (x, y, w, h))
    myfont = pygame.font.Font("images/Marline.otf", 45)
    my_text = myfont.render(text, True, (255, 255, 255))
    textRect = my_text.get_rect()
    textRect.center = (x+(w/2), y+(h/2))
    screen_surface.blit(my_text, textRect)

def create_pickle_file():
    with open("settings.data", "wb") as fic:
        pickle.dump(1, fic)

def sound_bool(sound_status):
    if sound_status == 1:
        return "On"
    elif sound_status == 0:
        return "Off"

def bg_static(screen_surface, bg):
    screen_surface.blit(bg, (0, 0))
    if functions.button(screen_surface, "Back", 100, 100, 100, 45, active_color, inactive_color):
        running = False

def open_settings(screen_surface):
    pygame.display.set_caption("modifie tes paramètres <3")
    screen_surface = pygame.display.set_mode((400, 300))
    
    bg = pygame.image.load("images/settings.jpg")
    screen_surface.blit(bg, (0, 0))    
    
    with open("settings.data", "rb") as fic:
        get_record = pickle.Unpickler(fic)
        sound_status = get_record.load()
    sound = sound_bool(sound_status)
    affichage(screen_surface, sound, 200, 25, 100, 45, black)

    
    running = True
    while running :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_click()
                running = False
                
        if functions.button(screen_surface, "Back", 100, 100, 100, 45, active_color, inactive_color):
            running = False                
        if functions.button(screen_surface, "Sound :", 100, 25, 100, 45, active_color, inactive_color):
            if sound_status or sound == 1:
                bg_static(screen_surface, bg)
                affichage(screen_surface, "Off", 200, 25, 100, 45, black)
                sound = 0
                pygame.mixer.pause()
            elif sound_status == 0 or sound == 0:
                bg_static(screen_surface, bg)
                affichage(screen_surface, "On", 200, 25, 100, 45, black)
                sound = 1
                pygame.mixer.unpause()
            
        with open("settings.data", "wb") as fic:
                record = pickle.Pickler(fic)
                record.dump(sound)
                                  
        pygame.display.update()