import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
pygame.mixer.init()

coin_sound = pygame.mixer.Sound("Coin.wav")
crash_sound = pygame.mixer.Sound("crash.wav")

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.jpg")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect  = self.image.get_rect()
        self.weight = random.randint(1, 3)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED / 2)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def relocate(self, coins_group):
        while True:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            if not any(self != coin and self.rect.colliderect(coin.rect) for coin in coins_group):
                break

P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group()
for _ in range(3):
    coins.add(Coin())

all_sprites = pygame.sprite.Group(P1, E1, *coins)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED:
            SPEED += 0.5

    DISPLAYSURF.blit(background, (0, 0))
    scores_text = font_small.render(str(SCORE), True, BLACK)
    coins_text  = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores_text, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    for coin in coins:
        if pygame.sprite.collide_rect(P1, coin):
            coin_sound.play()
            COINS += coin.weight
            coin.relocate(coins)
            if COINS % 5 == 0:
                SPEED += 1

    if pygame.sprite.spritecollideany(P1, enemies):
        crash_sound.play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)