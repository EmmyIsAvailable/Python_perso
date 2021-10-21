import pygame, functions, pickle

inactive_color = (0, 0, 0)
active_color = (50, 0, 0)
black = (0, 0, 0)

def sound_click(sound):
    if sound :
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
    sett_player = {"sound" : 1, "music" : 1}
    with open("settings.data", "wb") as fic:
        pickle.dump(sett_player, fic)

def sound_bool(sound_status):
    if sound_status == 1:
        return "On"
    elif sound_status == 0:
        return "Off"

def open_settings(screen_surface):
    screen_surface = pygame.display.set_mode((400, 300))
    
    bg = pygame.image.load("images/settings.jpg")
    screen_surface.blit(bg, (0, 0))    

    running = True
    while running :
        pygame.display.set_caption("modifie tes paramètres <3")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_click(sound)
                running = False
                
        with open("settings.data", "rb") as fic:
            get_record = pickle.Unpickler(fic)
            sett_status = get_record.load()
        sound = sett_status["sound"]
        volume = sett_status["music"]
        sound_status = sound_bool(sound)
        volume_status = sound_bool(volume)
        screen_surface.blit(bg, (0, 0))
        affichage(screen_surface, sound_status, 200, 15, 100, 45, black)
        affichage(screen_surface, volume_status, 200, 95, 100, 45, black)
       
        if functions.button(screen_surface, "Back", 100, 175, 100, 45, active_color, inactive_color, sound):
            running = False                
        if functions.button(screen_surface, "Sound :", 100, 15, 100, 45, active_color, inactive_color, sound):           
            if sound == 1:
                sound = 0
            elif sound == 0:
                sound = 1
        if functions.button(screen_surface, "Music :", 100, 95, 100, 45, active_color, inactive_color, sound):         
            if volume == 1:
                volume = 0
            elif volume == 0:
                volume = 1

        sett_player = {"sound" : sound, "music" : volume}
        with open("settings.data", "wb") as fic:
                record = pickle.Pickler(fic)
                record.dump(sett_player)
                
        pygame.event.wait()                          
        pygame.display.update()