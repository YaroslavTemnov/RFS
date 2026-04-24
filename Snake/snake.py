import pygame
import random
from pygame.locals import *

def control(direction):
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
    snake.insert(0,new_head)
    snake.pop()
    
def food_appearence():
    while True:
        pos1 = random.randrange(0, 600, 20)
        pos2 = random.randrange(0, 600, 20)
        pos = [pos1, pos2]
        if pos in snake:
            continue
        else:
            break
    return (pos1, pos2)

def check_self_collision():
    head = snake[0]
    for segment in snake[1:]:
        if head[0] == segment[0] and head[1] == segment[1]:
            return True
    return False

def growth():
    prelast = [snake[len(snake)-2][0], snake[len(snake)-2][1]]
    last = [snake[len(snake)-1][0], snake[len(snake)-1][1]]
    dir = (prelast[0] - last[0], prelast[1] - last[1])
    if dir == UP:
        snake.append([last[0] + DOWN[0], last[1] + DOWN[1]])
    elif dir == DOWN:
        snake.append([last[0] + UP[0], last[1] + UP[1]])
    elif dir == LEFT:
        snake.append([last[0] + RIGHT[0], last[1] + RIGHT[1]])
    elif dir == RIGHT:
        snake.append([last[0] + LEFT[0], last[1] + LEFT[1]])


pygame.init()
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
RUNNING = True
pygame.display.set_caption("Snake")

CELL_SIZE = 20
FPS = pygame.time.Clock()

UP = (0, -CELL_SIZE)
DOWN = (0, CELL_SIZE)
LEFT = (-CELL_SIZE, 0)
RIGHT = (CELL_SIZE, 0)

SQUARE = pygame.Surface((20, 20))
SQUARE.fill((0, 255, 0))
APPLE = pygame.Surface((20, 20))
APPLE.fill((255, 0, 0))
APPLE_POS = None


TIMED_APPLE = pygame.Surface((20, 20))
TIMED_APPLE.fill((255, 255, 0))
TIMED_APPLE_POS = None
TIMED_APPLE_APPEARENCE = pygame.USEREVENT + 1
TIMED_APPLE_DISAPPEARENCE = pygame.USEREVENT + 2
pygame.time.set_timer(TIMED_APPLE_APPEARENCE, 3000)

snake = [[300, 300], [300, 320]]
SCORE = 0

apple_hitbox = None
timed_apple_hitbox = None
direction = UP
next_direction = UP
speed = 100 

last_move = pygame.time.get_ticks()
font = pygame.font.Font(None, 20)

while RUNNING:
    current_time = pygame.time.get_ticks()
    snake_head = pygame.Rect(snake[0][0], snake[0][1], CELL_SIZE, CELL_SIZE)

    LVL = SCORE // 5
    speed = 100 - LVL * 5

    SCREEN.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                RUNNING = False
                pygame.quit() 
            elif event.key == pygame.K_w and direction != DOWN:
                next_direction = UP
            elif event.key == pygame.K_s and direction != UP:
                next_direction = DOWN
            elif event.key == pygame.K_a and direction != RIGHT:
                next_direction = LEFT
            elif event.key == pygame.K_d and direction != LEFT:
                next_direction = RIGHT
        elif event.type == TIMED_APPLE_APPEARENCE:
                TIMED_APPLE_POS = food_appearence()
                timed_apple_hitbox = pygame.Rect(TIMED_APPLE_POS[0], TIMED_APPLE_POS[1], CELL_SIZE, CELL_SIZE)
                pygame.time.set_timer(TIMED_APPLE_DISAPPEARENCE, 3000, True)
        elif event.type == TIMED_APPLE_DISAPPEARENCE:
            if TIMED_APPLE_POS:
                TIMED_APPLE_POS = None
                timed_apple_hitbox = None
                pygame.time.set_timer(TIMED_APPLE_DISAPPEARENCE, 0)
        elif event.type == pygame.QUIT:
            RUNNING = False



    if current_time - last_move >= speed:
        direction = next_direction
        control(direction)
        last_move = current_time

    info = f"score:{SCORE} \n level:{LVL}"
    font_label = font.render(info, True, (255,255,255))
    SCREEN.blit(font_label, (540, 20))

    for cell in snake:
        SCREEN.blit(SQUARE, (cell[0], cell[1]))

    if APPLE_POS:
        SCREEN.blit(APPLE, APPLE_POS)
    else:
        APPLE_POS = food_appearence()
        apple_hitbox = pygame.Rect(APPLE_POS[0], APPLE_POS[1], CELL_SIZE, CELL_SIZE)

    if snake_head.colliderect(apple_hitbox):
        APPLE_POS = None
        growth()
        SCORE += 1

    if TIMED_APPLE_POS:
        SCREEN.blit(TIMED_APPLE, TIMED_APPLE_POS)
        if snake_head.colliderect(timed_apple_hitbox):
            TIMED_APPLE_POS = None
            timed_apple_hitbox = None
            growth()
            SCORE += 3 
            pygame.time.set_timer(TIMED_APPLE_DISAPPEARENCE, 0) 


    if check_self_collision():
        RUNNING = False

    if snake_head[0] < 0 or snake_head[0] > 600:
        RUNNING = False
    if snake_head[1] < 0 or snake_head[1] > 600:
        RUNNING = False

    pygame.display.update()
    FPS.tick(60)

pygame.quit() 