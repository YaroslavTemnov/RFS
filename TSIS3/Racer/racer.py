import pygame, sys, json, os
from pygame.locals import *
import random, time

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

LIFE = 3
MONEY = 0
DISTANCE = 0
SPEED = 5
BASE_SPEED = 5
DIFFICULTY = "Normal"  
SOUND_ON = True
CAR_COLOR = "Red"

active_powerup = None
powerup_timer = 0
shield_active = False

font = pygame.font.SysFont("Verdana", 40) 
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 30)
font_title = pygame.font.SysFont("Verdana", 36) 


background = pygame.image.load("Racer/media/AnimatedStreet.png")
road = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

coin_sound = pygame.mixer.Sound('Racer/media/coin_pick_up.wav')
crash_sound = pygame.mixer.Sound('Racer/media/crash.wav')
powerup_sound = pygame.mixer.Sound('Racer/media/bonus.mp3')

def play_sound(sound):
    if SOUND_ON and sound:
        try:
            sound.play()
        except:
            pass

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Racer/media/coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
        self.value = 1

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.respawn()
    
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
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Hazard(pygame.sprite.Sprite):
    def __init__(self, hazard_type):
        super().__init__()
        self.type = hazard_type
        if hazard_type == "oil":
            self.image = pygame.image.load("Racer/media/oil.png")
        else:
            self.image = pygame.image.load("Racer/media/slow.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)
    
    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_type):
        super().__init__()
        self.type = power_type

        if power_type == "nitro":
            self.image = pygame.image.load("Racer/media/nitro.png")
        elif power_type == "shield":
            self.image = pygame.image.load("Racer/media/shield.png")
        else: 
            self.image = pygame.image.load("Racer/media/repair.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)
        self.spawn_time = pygame.time.get_ticks()
    
    def move(self):
        self.rect.move_ip(0, SPEED)
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 5000 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        if CAR_COLOR == "Red":
            self.image = pygame.image.load("Racer/media/Player_red.png").convert_alpha()
        else:
            self.image = pygame.image.load("Racer/media/Player_blue.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.speed_multiplier = 1.0
        self.slow_timer = 0
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        current_speed = 5
        if self.speed_multiplier != 1.0:
            current_speed = int(5 * self.speed_multiplier)
            
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-current_speed, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(current_speed, 0)
    
    def apply_hazard(self, hazard_type):
        if hazard_type == "slow":
            self.speed_multiplier = 0.5
            self.slow_timer = pygame.time.get_ticks()
        else:
            self.speed_multiplier = 2
            self.slow_timer = pygame.time.get_ticks()
    
    def update_hazards(self):
        if self.slow_timer and pygame.time.get_ticks() - self.slow_timer > 2000:
            self.speed_multiplier = 1.0
            self.slow_timer = 0

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
    
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = font_small.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

def save_leaderboard(entries):
    with open("leaderboard.json", "w") as f:
        json.dump(entries, f)

def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    return []

def add_score(name, score, distance):
    entries = load_leaderboard()
    entries.append({"name": name, "score": score, "distance": distance})
    entries.sort(key=lambda x: x["score"], reverse=True)
    entries = entries[:10]
    save_leaderboard(entries)
    return entries

def save_settings():
    settings = {"sound": SOUND_ON, "car_color": CAR_COLOR, "difficulty": DIFFICULTY}
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def load_settings():
    global SOUND_ON, CAR_COLOR, DIFFICULTY
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            settings = json.load(f)
            SOUND_ON = settings.get("sound", True)
            CAR_COLOR = settings.get("car_color", "Red")
            DIFFICULTY = settings.get("difficulty", "Normal")

def main_menu():
    global SPEED, BASE_SPEED, DIFFICULTY
    clock = pygame.time.Clock()
    
    play_btn = Button("Play", 100, 200, 200, 50, GREEN, (0, 200, 0))
    leaderboard_btn = Button("Leaderboard", 100, 270, 200, 50, BLUE, (0, 0, 200))
    settings_btn = Button("Settings", 100, 340, 200, 50, ORANGE, (200, 165, 0))
    quit_btn = Button("Quit", 100, 410, 200, 50, RED, (200, 0, 0))
    
    while True:
        DISPLAYSURF.fill(BLACK)
        title = font_title.render("RACING GAME", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        DISPLAYSURF.blit(title, title_rect)
        
        for btn in [play_btn, leaderboard_btn, settings_btn, quit_btn]:
            btn.draw(DISPLAYSURF)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if play_btn.is_clicked(event):
                return "play"
            if leaderboard_btn.is_clicked(event):
                leaderboard_screen()
            if settings_btn.is_clicked(event):
                settings_screen()
            if quit_btn.is_clicked(event):
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(FPS)

def settings_screen():
    global SOUND_ON, CAR_COLOR, DIFFICULTY
    clock = pygame.time.Clock()
    
    back_btn = Button("Back", 100, 500, 200, 50, RED, (200, 0, 0))
    sound_btn = Button(f"Sound: {'ON' if SOUND_ON else 'OFF'}", 100, 200, 200, 50, GRAY, (100, 100, 100))
    color_btn = Button(f"Car: {CAR_COLOR}", 100, 270, 200, 50, GRAY, (100, 100, 100))
    diff_btn = Button(f"Difficulty: {DIFFICULTY}", 100, 340, 200, 50, GRAY, (100, 100, 100))
    
    while True:
        DISPLAYSURF.fill(BLACK)
        title = font_medium.render("SETTINGS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        DISPLAYSURF.blit(title, title_rect)
        
        for btn in [sound_btn, color_btn, diff_btn, back_btn]:
            btn.draw(DISPLAYSURF)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if sound_btn.is_clicked(event):
                SOUND_ON = not SOUND_ON
                sound_btn.text = f"Sound: {'ON' if SOUND_ON else 'OFF'}"
                save_settings()
            if color_btn.is_clicked(event):
                CAR_COLOR = "Blue" if CAR_COLOR == "Red" else "Red"
                color_btn.text = f"Car: {CAR_COLOR}"
                save_settings()
            if diff_btn.is_clicked(event):
                difficulties = ["Easy", "Normal", "Hard"]
                idx = difficulties.index(DIFFICULTY)
                DIFFICULTY = difficulties[(idx + 1) % 3]
                diff_btn.text = f"Difficulty: {DIFFICULTY}"
                save_settings()
            if back_btn.is_clicked(event):
                return
        
        pygame.display.update()
        clock.tick(FPS)

def leaderboard_screen():
    clock = pygame.time.Clock()
    entries = load_leaderboard()
    back_btn = Button("Back", 100, 500, 200, 50, RED, (200, 0, 0))
    
    while True:
        DISPLAYSURF.fill(BLACK)
        title = font_medium.render("TOP 10 SCORES", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        DISPLAYSURF.blit(title, title_rect)
        
        y = 100
        for i, entry in enumerate(entries[:10]):
            text = f"{i+1}. {entry['name']} - Score: {entry['score']} - Dist: {entry['distance']}m"
            if len(text) > 35:
                text = text[:32] + "..."
            score_text = font_small.render(text, True, WHITE)
            DISPLAYSURF.blit(score_text, (20, y))
            y += 30
        
        if len(entries) == 0:
            no_scores = font_small.render("No scores yet! Play the game!", True, WHITE)
            no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH // 2, 200))
            DISPLAYSURF.blit(no_scores, no_scores_rect)
        
        back_btn.draw(DISPLAYSURF)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if back_btn.is_clicked(event):
                return
        
        pygame.display.update()
        clock.tick(FPS)

def game_over_screen(score, distance, coins):
    clock = pygame.time.Clock()
    
    retry_btn = Button("Retry", 100, 400, 200, 50, GREEN, (0, 200, 0))
    menu_btn = Button("Main Menu", 100, 470, 200, 50, BLUE, (0, 0, 200))
    
    while True:
        DISPLAYSURF.fill(RED)
        game_over_text = font.render("GAME OVER", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        DISPLAYSURF.blit(game_over_text, game_over_rect)
        
        score_text = font_medium.render(f"Score: {score}", True, WHITE)
        dist_text = font_medium.render(f"Distance: {distance}m", True, WHITE)
        coins_text = font_medium.render(f"Coins: {coins}", True, WHITE)
        
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        dist_rect = dist_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
        
        DISPLAYSURF.blit(score_text, score_rect)
        DISPLAYSURF.blit(dist_text, dist_rect)
        DISPLAYSURF.blit(coins_text, coins_rect)
        
        retry_btn.draw(DISPLAYSURF)
        menu_btn.draw(DISPLAYSURF)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if retry_btn.is_clicked(event):
                return "play"
            if menu_btn.is_clicked(event):
                return "menu"
        
        pygame.display.update()
        clock.tick(FPS)

def get_player_name():
    clock = pygame.time.Clock()
    name = ""
    input_active = True
    
    while input_active:
        DISPLAYSURF.fill(BLACK)
        prompt = font_medium.render("Enter your name:", True, WHITE)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 180))
        DISPLAYSURF.blit(prompt, prompt_rect)
        
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 230, 200, 40)
        pygame.draw.rect(DISPLAYSURF, WHITE, input_rect, 2)
        name_surface = font_medium.render(name, True, WHITE)
        name_rect = name_surface.get_rect(center=input_rect.center)
        DISPLAYSURF.blit(name_surface, name_rect)

        if pygame.time.get_ticks() % 1000 < 500:
            cursor_rect = pygame.Rect(name_rect.right + 2, name_rect.top, 2, name_rect.height)
            pygame.draw.rect(DISPLAYSURF, WHITE, cursor_rect)
        
        instruction = font_small.render("Press ENTER to continue", True, GRAY)
        inst_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 320))
        DISPLAYSURF.blit(instruction, inst_rect)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name:
                    return name
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15 and event.unicode.isprintable():
                        name += event.unicode
        
        pygame.display.update()
        clock.tick(FPS)

def game_loop():
    global MONEY, DISTANCE, SPEED, BASE_SPEED, LIFE, active_powerup, powerup_timer, shield_active
    
    player_name = get_player_name()
    MONEY = 0
    DISTANCE = 0
    SPEED = BASE_SPEED
    active_powerup = None
    powerup_timer = 0
    shield_active = False
    LIFE = 3
    if DIFFICULTY == "Easy":
        BASE_SPEED = 4
    elif DIFFICULTY == "Normal":
        BASE_SPEED = 5
    else:  # Hard
        BASE_SPEED = 7
    SPEED = BASE_SPEED
    
    P1 = Player()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    hazards = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    for _ in range(3):
        enemies.add(Enemy())
    coins.add(Coin())
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    for enemy in enemies:
        all_sprites.add(enemy)
    for coin in coins:
        all_sprites.add(coin)
    
    INC_SPEED = pygame.USEREVENT + 1
    SPAWN_HAZARD = pygame.USEREVENT + 2
    SPAWN_POWERUP = pygame.USEREVENT + 3
    
    pygame.time.set_timer(INC_SPEED, 3000)
    pygame.time.set_timer(SPAWN_HAZARD, 5000)
    pygame.time.set_timer(SPAWN_POWERUP, 8000)
    

    y1 = 0
    y2 = -SCREEN_HEIGHT
    last_distance_update = pygame.time.get_ticks()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.3
            if event.type == SPAWN_HAZARD and random.random() < 0.4:
                hazard_type = random.choice(["oil", "slow"])
                hazard = Hazard(hazard_type)
                if not pygame.sprite.collide_rect(hazard, P1):
                    hazards.add(hazard)
                    all_sprites.add(hazard)
            if event.type == SPAWN_POWERUP and random.random() < 0.3:
                power_type = random.choice(["nitro", "shield", "repair"])
                powerup = PowerUp(power_type)
                if not pygame.sprite.collide_rect(powerup, P1):
                    powerups.add(powerup)
                    all_sprites.add(powerup)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if active_powerup:
            if pygame.time.get_ticks() - powerup_timer > 5000:
                if active_powerup == "nitro":
                    SPEED = BASE_SPEED  + 3
                elif active_powerup == "shield":
                    shield_active = False
                active_powerup = None
        
        current_time = pygame.time.get_ticks()
        if current_time - last_distance_update > 100:
            DISTANCE += 1
            last_distance_update = current_time
        
        y1 += SPEED
        y2 += SPEED
        if y1 > SCREEN_HEIGHT:
            y1 = -SCREEN_HEIGHT
        if y2 > SCREEN_HEIGHT:
            y2 = -SCREEN_HEIGHT
        
        DISPLAYSURF.blit(road, (0, y1))
        DISPLAYSURF.blit(road, (0, y2))
        
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
        
        P1.update_hazards()
        P1.move()
        
        total_score = MONEY + DISTANCE // 10
        score_display = font_small.render(f"Score: {total_score}", True, BLACK)
        coins_display = font_small.render(f"Coins: {MONEY}", True, BLACK)
        dist_display = font_small.render(f"Dist: {DISTANCE}m", True, BLACK)
        speed_display = font_small.render(f"Speed: {int(SPEED)}", True, BLACK)
        life_display = font_small.render(f"Life: {int(LIFE)}", True, BLACK)       
        DISPLAYSURF.blit(score_display, (10, 10))
        DISPLAYSURF.blit(coins_display, (10, 30))
        DISPLAYSURF.blit(dist_display, (10, 50))
        DISPLAYSURF.blit(speed_display, (10, 70))
        DISPLAYSURF.blit(life_display, (10, 90))        
        if active_powerup:
            time_left = max(0, 5 - (pygame.time.get_ticks() - powerup_timer)//1000)
            power_text = font_small.render(f"{active_powerup.upper()}: {time_left}s", True, BLUE)
            DISPLAYSURF.blit(power_text, (250, 10))
        
        collided_coin = pygame.sprite.spritecollideany(P1, coins)
        if collided_coin:
            play_sound(coin_sound)
            MONEY += collided_coin.value
            collided_coin.respawn()
        
        collided_powerup = pygame.sprite.spritecollideany(P1, powerups)
        if collided_powerup:
            play_sound(powerup_sound)
            if collided_powerup.type == "nitro":
                if active_powerup != "nitro":
                    SPEED = BASE_SPEED + 5
                active_powerup = "nitro"
                powerup_timer = pygame.time.get_ticks()
            elif collided_powerup.type == "shield":
                shield_active = True
                active_powerup = "shield"
                powerup_timer = pygame.time.get_ticks()
            elif collided_powerup.type == "repair":
                if LIFE < 3:
                    LIFE += 1
            collided_powerup.kill()
        
        for powerup in powerups:
            if powerup.is_expired():
                powerup.kill()
        
        collided_hazard = pygame.sprite.spritecollideany(P1, hazards)
        if collided_hazard:
            P1.apply_hazard(collided_hazard.type)
            collided_hazard.kill()
        
        if pygame.sprite.spritecollideany(P1, enemies):
            if shield_active:
                shield_active = False
                active_powerup = None
                collided_enemy = pygame.sprite.spritecollideany(P1, enemies)
                if collided_enemy:
                    collided_enemy.kill()
                    new_enemy = Enemy()   
                    enemies.add(new_enemy) 
                    all_sprites.add(new_enemy)    
                    if SOUND_ON:
                        shield_break = pygame.mixer.Sound('Racer/media/shield_break.mp3')
                        shield_break.play()
            elif LIFE > 1:
                if SOUND_ON:
                    play_sound(crash_sound)
                LIFE -= 1
                collided_enemy = pygame.sprite.spritecollideany(P1, enemies)
                if collided_enemy:
                    collided_enemy.kill()
                    new_enemy = Enemy()   
                    enemies.add(new_enemy) 
                    all_sprites.add(new_enemy)               
            else:
                play_sound(crash_sound)
                total_score = MONEY + DISTANCE // 10
                add_score(player_name, total_score, DISTANCE)
                
                time.sleep(0.5)
                result = game_over_screen(total_score, DISTANCE, MONEY)
                if result == "play":
                    return game_loop()
                else:
                    return
        
        pygame.display.update()
        FramePerSec.tick(FPS)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game")
load_settings()

while True:
    result = main_menu()
    if result == "play":
        game_loop()