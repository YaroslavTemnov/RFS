import pygame


pygame.init()
WIDTH, HEIGHT = 600, 600
FPS = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
pygame.display.set_caption("Ball game")
MOVEMENT_SPEED = 20
x, y = 100, 100
while running:
    screen.fill((255,255,255))
    circle = pygame.draw.circle(screen, (255,0,0), (x, y), 25)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:    
            running = False
            pygame.quit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and y < 580:
                y += MOVEMENT_SPEED
            if event.key == pygame.K_UP and y > 20:
                y -= MOVEMENT_SPEED
            if event.key == pygame.K_RIGHT and x < 580:
                x += MOVEMENT_SPEED
            if event.key == pygame.K_LEFT and x > 20:
                x -= MOVEMENT_SPEED
                
    FPS.tick(60)