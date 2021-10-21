import pygame, functions, settings, os, pickle

pygame.init()
mainClock = pygame.time.Clock()
settings.create_pickle_file()

res = (800, 645)
inactive_color = (200, 0, 0)
active_color = (255, 0, 0)

screen_surface = pygame.display.set_mode(res)

launched = True
play_bool = 0
sett_bool = 0

while launched:
    pygame.display.set_caption("ecrase un chat")
    accueil_img = pygame.image.load("images/accueil.jpg")
    screen_surface.blit(accueil_img, (0, 0))
    
    with open("settings.data", "rb") as fic:
        get_record = pickle.Unpickler(fic)
        sett_status = get_record.load()
    volume = sett_status["music"]
    sound = sett_status["sound"]
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove("settings.data")
            launched = False
    if play_bool :
        functions.ft_jouer(screen_surface, volume)
        screen_surface = pygame.display.set_mode(res)
        pygame.mixer.music.stop()
        play_bool = 0
    if sett_bool :
        settings.open_settings(screen_surface)
        screen_surface = pygame.display.set_mode(res)
        sett_bool = 0
    
    if functions.button(screen_surface, "Play", 0, 600, 250, 45, active_color, inactive_color, sound):
        play_bool = 1
    if functions.button(screen_surface, "Settings", 275, 600, 250, 45, active_color, inactive_color, sound):
        sett_bool = 1
    if functions.button(screen_surface, "Quit", 550, 600, 250, 45, active_color, inactive_color, sound):
        os.remove("settings.data")
        pygame.quit()
        
    pygame.display.update()
    mainClock.tick(60)