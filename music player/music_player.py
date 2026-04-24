import pygame
import os

pygame.init()
WIDTH, HEIGHT = 900, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
pygame.display.set_caption("Music player")
pause = False
songs = os.listdir("music player/songs")
song = 0
music = pygame.mixer.Sound("music player/songs/"+songs[song])
music_on = False

while running:
    screen.fill((0,0,0))
    font = pygame.font.Font(None, 50)
    info = f"song:{song+1}.{songs[song]}"
    font_label = font.render(info, True, (255,255,255))

    screen.blit(font_label, (10,50))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not(music_on):
                music.play()
                music_on = True
            elif event.key == pygame.K_s:
                if pause == True:
                    pygame.mixer.unpause()
                    pause = False
                elif pause == False:
                    pygame.mixer.pause()
                    pause = True

            elif event.key == pygame.K_n:
                if song == 8:
                    song = 0
                else:
                    song += 1
                music.stop()
                music = pygame.mixer.Sound("music player/songs/"+songs[song])
                music.play()

            elif event.key == pygame.K_b:
                if song == 0:
                    song = 8
                else:
                    song -= 1
                music.stop()
                music = pygame.mixer.Sound("music player/songs/"+songs[song])
                music.play()
            elif event.key == pygame.K_q:
                running = False
                pygame.quit() 


        elif event.type == pygame.QUIT:
            running = False
            pygame.quit() 
