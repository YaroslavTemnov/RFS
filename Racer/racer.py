import pygame, sys
from pygame.locals import *
import random, time
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

MONEY = 0
SCORE_INFO = f"score:{MONEY}"
LVL = MONEY // 3
SPEED = 5 + LVL

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("Racer/media/AnimatedStreet.png")
road = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")



class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Racer/media/coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def respawn(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Racer/media/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Racer/media/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                         
P1 = Player()
E1 = Enemy()
C1 = Coin()
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)




while True:

    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.blit(road, (0,0))
    DISPLAYSURF.blit(road, (400,0))
    scores = font_small.render(str(MONEY), True, BLACK)
    DISPLAYSURF.blit(scores, (380,10))
 
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    if pygame.sprite.spritecollideany(P1, coins):
          pygame.mixer.Sound('Racer/media/coin_pick_up.wav').play()
          MONEY += 1
          collided_coin = pygame.sprite.spritecollideany(P1, coins)
          if collided_coin:
            collided_coin.respawn() 
          pygame.display.update()

 
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('Racer/media/crash.wav').play()
          time.sleep(0.5)
    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()

    FramePerSec.tick(FPS)