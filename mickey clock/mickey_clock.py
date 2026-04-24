import pygame
import datetime


def rotation(image, angle, centre):
    rotating_hand = pygame.transform.rotate(image, -angle)
    rect = rotating_hand.get_rect(center = centre)
    return rotating_hand, rect


pygame.init()
WIDTH, HEIGHT = 800, 615
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
pygame.display.set_caption("Mickey's clock")

clock = pygame.image.load('mickey clock/images/Mickey without hands.jpg')
clock_sized = pygame.transform.scale(clock, (WIDTH, HEIGHT))

right_hand = pygame.image.load('mickey clock/images/right_hand.png')
left_hand = pygame.image.load('mickey clock/images/left_hand.png')

right_hand_sized = pygame.transform.scale(right_hand, (300, 550))
left_hand_sized = pygame.transform.scale(left_hand, (250, 570))

FPS = pygame.time.Clock()

while running:
    pygame.display.update()

    now = datetime.datetime.now()
    minutes_angle = now.minute * 6 
    seconds_angle = now.second * 6

    screen.blit(clock_sized, (0, 0))


    rotating_right, right_pos = rotation(right_hand_sized, seconds_angle, (400, 307))
    rotating_left, left_pos = rotation(left_hand_sized, minutes_angle, (400, 307))
    screen.blit(rotating_right, right_pos)
    screen.blit(rotating_left, left_pos)

    FPS.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
