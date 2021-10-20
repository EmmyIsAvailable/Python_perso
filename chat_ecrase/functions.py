import pygame, settings, random
from pygame.locals import *

inactive_color = (200, 0, 0)
active_color = (255, 0, 0)

def button(screen_surface, text, x, y, w, h, active_color, inactive_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    pressed = False
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen_surface, active_color, (x, y, w, h))
        if click[0] == 1:
            pressed = True
            settings.sound_click()
            return pressed
    else:
        pygame.draw.rect(screen_surface, inactive_color, (x, y, w, h))
    
    myfont = pygame.font.Font("images/Marline.otf", 45)
    button_text = myfont.render(text, True, (255, 255, 255))
    textRect = button_text.get_rect()
    textRect.center = (x+(w/2), y+(h/2))
    screen_surface.blit(button_text, textRect)
    return pressed

class Player:
    def __init__(self, x, y, name):
        self.image = pygame.image.load("images/"+name+".png")
        
        self.pos_x = 0
        self.pos_y = 0
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
    
    def left(self):
        self.pos_x = -32
        
    def right(self):
        self.pos_x = 32
    
    def up(self):
        self.pos_y = -43
        
    def down(self):
        self.pos_y = 43

    def draw(self, screen_surface):
        screen_surface.blit(self.image, self.rect)
    
    def collision_x(self, plateau, screen_surface, volume):
        for obstacle in plateau.collisionList:
            if obstacle.rect.colliderect(self.rect):
                if isinstance (obstacle, Obstacle):
                    if self.pos_x > 0:
                        self.rect.right = obstacle.rect.left
                    elif self.pos_x < 0:
                        self.rect.left = obstacle.rect.right
                elif isinstance (obstacle, Player):
                    failure_screen(screen_surface, volume)
                    return False
        return True
                
    def collision_y(self, plateau, screen_surface, volume):
        for obstacle in plateau.collisionList:
            if obstacle.rect.colliderect(self.rect):
                if isinstance (obstacle, Obstacle):
                    if self.pos_y > 0:
                        self.rect.bottom = obstacle.rect.top
                    elif self.pos_y < 0:
                        self.rect.top = obstacle.rect.bottom
                elif isinstance (obstacle, Player):
                    failure_screen(screen_surface, volume)
                    return False
        return True

def failure_screen(screen_surface, volume):
    aff = True
    screen_fail = pygame.image.load("images/gameover.png")
    pygame.mixer.music.load("sounds/failure.mp3")
    pygame.mixer.music.set_volume(0.5 * int(volume))
    pygame.mixer.music.play(-1)
    while aff:
        screen_surface.blit(screen_fail, (0, 0))
        pygame.display.set_caption("dommage")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                aff = False
        if button(screen_surface, "Ok", 400, 450, 70, 45, (50, 0, 0), (0, 0, 0)):
            aff = False
        pygame.display.update()
        
class Obstacle:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.image = pygame.image.load("images/cupcake.png")
        self.rect = self.image.get_rect()
        self.rect.left = (self.x)*32
        self.rect.bottom = (self.y)*43
    
    def draw(self, screen_surface):
        screen_surface.blit(self.image, self.rect)
        
class Plateau:
    def __init__(self):
        self.name = "plateau.txt"
        self.list_plein = []
        self.collisionList = []
    
    def read_txt(self):
        fichier = open(self.name, 'r')
        tmp = list(fichier)
        
        plateau = []
        for ligne in tmp:
            plateau += [list(ligne)]
        
        for i in range(len(plateau) - 1):
            plateau[i].pop()
            
        return plateau
    
    def create_collisionList(self, screen_surface):
        self.list_plein = self.read_txt()
        
        for j in range(len(self.list_plein)):
            for i in range(len(self.list_plein[j])):
                if self.list_plein[j][i] == 'p':
                    obstacle = Obstacle(i, j, 'p')
                    self.collisionList.append(obstacle)
                    obstacle.draw(screen_surface)
                    
    def spawn_ennemy(self, screen_surface, nb_ennemy):
        ennemy = 0
        self.list_plein = self.read_txt() 
        ennemy_list = []
        
        while ennemy != nb_ennemy:
            j = random.randint(1, len(self.list_plein)-1)
            i = random.randint(1, len(self.list_plein[0])-1)
            if self.list_plein[j][i] == 'v':
                chat_pain = Player((i * 32), (j * 43), "mechant_chat_pain_")
                self.collisionList.append(chat_pain)
                ennemy_list.append(chat_pain)
                ennemy += 1
        return ennemy_list
                
def ft_jouer(screen_surface, volume):
    screen_surface = pygame.display.set_mode((870,645))
    accueil_img = pygame.image.load("images/background.jpg")
    player = Player(0, 43, "boulanger_")
    player.draw(screen_surface)
    plateau = Plateau()
    ennemy_list = plateau.spawn_ennemy(screen_surface, 1)
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.set_volume(0.25 * int(volume))
    pygame.mixer.music.play(-1) 
    
    running_game = True
    while running_game:
        pygame.display.set_caption("maintenant, écrase les chats...")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.left()
                    player.rect.x += player.pos_x
                    running_game = player.collision_x(plateau, screen_surface, volume)
                if event.key == K_RIGHT:
                    player.right()
                    player.rect.x += player.pos_x
                    running_game = player.collision_x(plateau, screen_surface, volume)
                if event.key == K_UP:
                    player.up()
                    player.rect.y += player.pos_y
                    running_game = player.collision_y(plateau, screen_surface, volume)
                if event.key == K_DOWN:
                    player.down()
                    player.rect.y += player.pos_y
                    running_game = player.collision_y(plateau, screen_surface, volume)
 
        screen_surface.blit(accueil_img, (0, 0))
        plateau.create_collisionList(screen_surface)
        player.draw(screen_surface)
        for i in ennemy_list:
            i.draw(screen_surface)
        
        if button(screen_surface, "Back", 800, 0, 70, 45, active_color, inactive_color):
            running_game = False
        
        pygame.display.update()