import pygame, settings
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
    
    def collision_x(self, plateau):
        for obstacle in plateau.collisionList:
            if obstacle.rect.colliderect(self.rect):
                if self.pos_x > 0:
                    self.rect.right = obstacle.rect.left
                elif self.pos_x < 0:
                    self.rect.left = obstacle.rect.right

    def collision_y(self, plateau):
        for obstacle in plateau.collisionList:
            if obstacle.rect.colliderect(self.rect):
                if self.pos_y > 0:
                    self.rect.bottom = obstacle.rect.top
                if self.pos_y < 0:
                    self.rect.top = obstacle.rect.bottom

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

def ft_jouer(screen_surface):
    screen_surface = pygame.display.set_mode((870,645))
    accueil_img = pygame.image.load("images/background.jpg")
    player = Player(0, 43, "boulanger_")
    player.draw(screen_surface)
    plateau = Plateau()
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1) 
    
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.left()
                    player.rect.x += player.pos_x
                    player.collision_x(plateau)
                if event.key == K_RIGHT:
                    player.right()
                    player.rect.x += player.pos_x
                    player.collision_x(plateau)
                if event.key == K_UP:
                    player.up()
                    player.rect.y += player.pos_y
                    player.collision_y(plateau)
                if event.key == K_DOWN:
                    player.down()
                    player.rect.y += player.pos_y
                    player.collision_y(plateau)
 
        screen_surface.blit(accueil_img, (0, 0))
        plateau.create_collisionList(screen_surface)
        player.draw(screen_surface)
        
        if button(screen_surface, "Back", 800, 0, 70, 45, active_color, inactive_color):
            running_game = False
        
        pygame.display.update()
