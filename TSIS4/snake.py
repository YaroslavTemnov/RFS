import pygame, random, json, os
from pygame.locals import *
from connect import connect


SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid_overlay": True,
    "sound": True
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def get_or_create_player(username, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cursor.fetchone()
    if player:
        player_id = player[0]
    else:
        cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        player_id = cursor.fetchone()[0]
        conn.commit()
    cursor.close()
    return player_id

def save_game_result(player_id, score, level_reached, conn):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
        (player_id, score, level_reached)
    )
    conn.commit()
    cursor.close()

def get_personal_best(player_id, conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
        (player_id,)
    )
    best = cursor.fetchone()[0]
    cursor.close()
    return best if best is not None else 0

def get_top_10_scores(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    top = cursor.fetchall()
    cursor.close()
    return top


def control(direction):
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
    snake.insert(0, new_head)
    snake.pop()

TIMED_APPLE_APPEARENCE = pygame.USEREVENT + 1
TIMED_APPLE_DISAPPEARENCE = pygame.USEREVENT + 2

def food_appearence(obstacles=None):
    while True:
        pos1 = random.randrange(0, 600, 20)
        pos2 = random.randrange(0, 600, 20)
        pos = [pos1, pos2]
        if pos in snake:
            continue
        if obstacles and pos in obstacles:
            continue
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
def shorten_snake(segments=2):
    for _ in range(segments):
        if len(snake) > 1:
            snake.pop()

POWERUP_TYPES = ["speed_boost", "slow_motion", "shield"]
POWERUP_DURATION = 5000  
POWERUP_LIFESPAN = 8000  

class PowerUp:
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type
        self.spawn_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > POWERUP_LIFESPAN

def generate_obstacles(level, snake_head_pos, count=5):
    if level < 3:
        return []
    obstacles = []
    attempts = 0
    while len(obstacles) < count and attempts < 100:
        x = random.randrange(0, 600, 20)
        y = random.randrange(0, 600, 20)
        pos = [x, y]
        if pos in snake or pos == snake_head_pos:
            attempts += 1
            continue
        obstacles.append(pos)
    return obstacles


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def draw_text_button(screen, text, x, y, font, color=(255,255,255), bg=None):
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect(center=(x, y))
    if bg:
        pygame.draw.rect(screen, bg, rect.inflate(20, 10))
    screen.blit(text_surf, rect)
    return rect

def main_menu(screen, font):
    clock = pygame.time.Clock()
    while True:
        screen.fill((0,0,0))
        title = font.render("SNAKE GAME", True, (255,255,0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        play_rect = draw_text_button(screen, "PLAY", WIDTH//2, 250, font, (255,255,255), (50,50,50))
        leaderboard_rect = draw_text_button(screen, "LEADERBOARD", WIDTH//2, 320, font)
        settings_rect = draw_text_button(screen, "SETTINGS", WIDTH//2, 390, font)
        quit_rect = draw_text_button(screen, "QUIT", WIDTH//2, 460, font)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return "play"
                if leaderboard_rect.collidepoint(event.pos):
                    return "leaderboard"
                if settings_rect.collidepoint(event.pos):
                    return "settings"
                if quit_rect.collidepoint(event.pos):
                    return "quit"
        clock.tick(30)

def leaderboard_screen(screen, font, conn):
    top = get_top_10_scores(conn)
    clock = pygame.time.Clock()
    while True:
        screen.fill((0,0,0))
        title = font.render("TOP 10 SCORES", True, (255,255,0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        y = 80
        for i, row in enumerate(top):
            username, score, level, played_at = row
            text = f"{i+1}. {username}  Score:{score}  Level:{level}  {played_at.strftime('%Y-%m-%d')}"
            label = font.render(text, True, (200,200,200))
            screen.blit(label, (50, y))
            y += 30
        back_rect = draw_text_button(screen, "BACK", WIDTH//2, HEIGHT-50, font, (255,255,255), (100,0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                return
        clock.tick(30)

def settings_screen(screen, font, current_settings):
    settings = current_settings.copy()
    clock = pygame.time.Clock()
    color_options = [(0,255,0), (255,0,0), (0,0,255), (255,255,0)]
    color_index = color_options.index(tuple(settings["snake_color"])) if tuple(settings["snake_color"]) in color_options else 0
    while True:
        screen.fill((0,0,0))
        y = 50
        draw_text_button(screen, "SETTINGS", WIDTH//2, y, font, (255,255,0))
        y += 60
        grid_text = f"Grid Overlay: {'ON' if settings['grid_overlay'] else 'OFF'}"
        grid_rect = draw_text_button(screen, grid_text, WIDTH//2, y, font)
        y += 50
        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        sound_rect = draw_text_button(screen, sound_text, WIDTH//2, y, font)
        y += 50
        color_text = f"Snake Color: {settings['snake_color']}"
        color_rect = draw_text_button(screen, color_text, WIDTH//2, y, font)
        y += 80
        save_rect = draw_text_button(screen, "SAVE & BACK", WIDTH//2, y, font, (0,255,0), (50,50,50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", settings
            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_rect.collidepoint(event.pos):
                    settings["grid_overlay"] = not settings["grid_overlay"]
                elif sound_rect.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                elif color_rect.collidepoint(event.pos):
                    color_index = (color_index + 1) % len(color_options)
                    settings["snake_color"] = list(color_options[color_index])
                elif save_rect.collidepoint(event.pos):
                    return "back", settings
        clock.tick(30)

def game_over_screen(screen, font, score, level, personal_best):
    clock = pygame.time.Clock()
    while True:
        screen.fill((0,0,0))
        texts = [
            f"GAME OVER",
            f"Score: {score}",
            f"Level: {level}",
            f"Personal Best: {personal_best}"
        ]
        y = 150
        for t in texts:
            surf = font.render(t, True, (255,255,255))
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += 50
        retry_rect = draw_text_button(screen, "RETRY", WIDTH//2 - 80, y, font, (0,255,0))
        menu_rect = draw_text_button(screen, "MAIN MENU", WIDTH//2 + 80, y, font, (255,0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return "retry"
                if menu_rect.collidepoint(event.pos):
                    return "menu"
        clock.tick(30)

def run_game(username, player_id, conn, settings):
    font = pygame.font.SysFont("Verdana", 40) 
    global snake, SCORE, direction, next_direction, last_move
    global APPLE_POS, apple_hitbox, TIMED_APPLE_POS, timed_apple_hitbox
    global TIMED_APPLE_APPEARENCE, TIMED_APPLE_DISAPPEARENCE

    snake = [[300, 300], [300, 320]]
    SCORE = 0
    direction = UP
    next_direction = UP
    last_move = pygame.time.get_ticks()
    
    active_powerup = None
    powerup_end_time = 0
    shield_active = False
    current_speed_modifier = 1.0
    
    poison_pos = None
    poison_rect = None
    POISON_APPEAR = pygame.USEREVENT + 5
    pygame.time.set_timer(POISON_APPEAR, 5000)
    
    obstacles = []
    
    APPLE_POS = None
    apple_hitbox = None
    TIMED_APPLE_POS = None
    timed_apple_hitbox = None
    pygame.time.set_timer(TIMED_APPLE_APPEARENCE, 3000)
    pygame.time.set_timer(TIMED_APPLE_DISAPPEARENCE, 0)
    
    powerup_on_field = None
    POWERUP_SPAWN = pygame.USEREVENT + 6
    pygame.time.set_timer(POWERUP_SPAWN, 10000)
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        current_time = pygame.time.get_ticks()
        level = SCORE // 5
        
        base_speed = max(30, 100 - level * 5)
        if active_powerup:
            if active_powerup == "speed_boost":
                current_speed_modifier = 0.6
            elif active_powerup == "slow_motion":
                current_speed_modifier = 1.8
            else:
                current_speed_modifier = 1.0
            if current_time > powerup_end_time:
                active_powerup = None
                current_speed_modifier = 1.0
        else:
            current_speed_modifier = 1.0
        
        speed = int(base_speed * current_speed_modifier)
        
        if level >= 3 and len(obstacles) == 0:
            obstacles = generate_obstacles(level, snake[0])
        
        SCREEN.fill((0,0,0))
        if settings["grid_overlay"]:
            draw_grid(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    return "quit"
                elif event.key == pygame.K_w and direction != DOWN:
                    next_direction = UP
                elif event.key == pygame.K_s and direction != UP:
                    next_direction = DOWN
                elif event.key == pygame.K_a and direction != RIGHT:
                    next_direction = LEFT
                elif event.key == pygame.K_d and direction != LEFT:
                    next_direction = RIGHT
            elif event.type == TIMED_APPLE_APPEARENCE:
                TIMED_APPLE_POS = food_appearence(obstacles)
                timed_apple_hitbox = pygame.Rect(TIMED_APPLE_POS[0], TIMED_APPLE_POS[1], CELL_SIZE, CELL_SIZE)
                pygame.time.set_timer(TIMED_APPLE_DISAPPEARENCE, 3000, True)
            elif event.type == TIMED_APPLE_DISAPPEARENCE:
                TIMED_APPLE_POS = None
                timed_apple_hitbox = None
            elif event.type == POISON_APPEAR and not poison_pos:
                poison_pos = food_appearence(obstacles)
                poison_rect = pygame.Rect(poison_pos[0], poison_pos[1], CELL_SIZE, CELL_SIZE)
            elif event.type == POWERUP_SPAWN and not powerup_on_field:
                ptype = random.choice(POWERUP_TYPES)
                pos = food_appearence(obstacles)
                powerup_on_field = PowerUp(pos, ptype)
            elif event.type == pygame.QUIT:
                running = False
                return "quit"
        
        if current_time - last_move >= speed:
            direction = next_direction
            control(direction)
            last_move = current_time
        
        head_rect = pygame.Rect(snake[0][0], snake[0][1], CELL_SIZE, CELL_SIZE)
        
        if APPLE_POS is None:
            APPLE_POS = food_appearence(obstacles)
            apple_hitbox = pygame.Rect(APPLE_POS[0], APPLE_POS[1], CELL_SIZE, CELL_SIZE)
        if head_rect.colliderect(apple_hitbox):
            APPLE_POS = None
            growth()
            SCORE += 1
        
        if TIMED_APPLE_POS and head_rect.colliderect(timed_apple_hitbox):
            TIMED_APPLE_POS = None
            timed_apple_hitbox = None
            growth()
            SCORE += 3
            pygame.time.set_timer(TIMED_APPLE_DISAPPEARENCE, 0)
        
        if poison_pos and head_rect.colliderect(poison_rect):
            poison_pos = None
            shorten_snake(2)
            if len(snake) <= 1:
                running = False
        
        if powerup_on_field and head_rect.colliderect(powerup_on_field.rect):
            active_powerup = powerup_on_field.type
            powerup_end_time = current_time + POWERUP_DURATION
            if active_powerup == "shield":
                shield_active = True
            powerup_on_field = None

        if powerup_on_field and powerup_on_field.expired():
            powerup_on_field = None
        
        if snake[0] in obstacles:
            if shield_active:
                shield_active = False
                active_powerup = None
            else:
                running = False
        
        if check_self_collision():
            if shield_active:
                shield_active = False
                active_powerup = None
            else:
                running = False
        if snake[0][0] < 0 or snake[0][0] >= WIDTH or snake[0][1] < 0 or snake[0][1] >= HEIGHT:
            if shield_active:
                shield_active = False
                active_powerup = None
                snake[0][0] = max(0, min(WIDTH-20, snake[0][0]))
                snake[0][1] = max(0, min(HEIGHT-20, snake[0][1]))
            else:
                running = False
        
        snake_color = tuple(settings["snake_color"])
        for cell in snake:
            pygame.draw.rect(SCREEN, snake_color, (cell[0], cell[1], CELL_SIZE, CELL_SIZE))
        
        # Draw food
        if APPLE_POS:
            pygame.draw.rect(SCREEN, (255,0,0), (APPLE_POS[0], APPLE_POS[1], CELL_SIZE, CELL_SIZE))
        if TIMED_APPLE_POS:
            pygame.draw.rect(SCREEN, (255,255,0), (TIMED_APPLE_POS[0], TIMED_APPLE_POS[1], CELL_SIZE, CELL_SIZE))
        if poison_pos:
            pygame.draw.rect(SCREEN, (139,0,0), (poison_pos[0], poison_pos[1], CELL_SIZE, CELL_SIZE))
        if powerup_on_field:
            color = (0,255,255) if powerup_on_field.type == "speed_boost" else (255,0,255) if powerup_on_field.type == "slow_motion" else (0,255,255)
            pygame.draw.rect(SCREEN, color, powerup_on_field.rect)
        
        for obs in obstacles:
            pygame.draw.rect(SCREEN, (100,100,100), (obs[0], obs[1], CELL_SIZE, CELL_SIZE))
        
        info = f"Score:{SCORE}  Level:{level}  Best:{get_personal_best(player_id, conn)}"
        font_label = font.render(info, True, (255,255,255))
        SCREEN.blit(font_label, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    final_level = SCORE // 5
    save_game_result(player_id, SCORE, final_level, conn)
    personal_best = get_personal_best(player_id, conn)
    return ("game_over", SCORE, final_level, personal_best)

def main():
    pygame.init()
    global WIDTH, HEIGHT, SCREEN, CELL_SIZE, UP, DOWN, LEFT, RIGHT, FPS
    WIDTH, HEIGHT = 600, 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    CELL_SIZE = 20
    UP = (0, -CELL_SIZE)
    DOWN = (0, CELL_SIZE)
    LEFT = (-CELL_SIZE, 0)
    RIGHT = (CELL_SIZE, 0)
    font = pygame.font.Font(None, 30)
    
    settings = load_settings()
    conn = connect()
    if not conn:
        print("DB connection failed")
        return

    username = ""
    input_active = True
    while input_active:
        SCREEN.fill((0,0,0))
        prompt = font.render("Enter your username:", True, (255,255,255))
        SCREEN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 200))
        name_surf = font.render(username + "_", True, (0,255,0))
        SCREEN.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, 250))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False
                conn.close()
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        pygame.time.delay(50)
    
    player_id = get_or_create_player(username, conn)
    
    while True:
        action = main_menu(SCREEN, font)
        if action == "play":
            result = run_game(username, player_id, conn, settings)
            if result[0] == "quit":
                break
            elif result[0] == "game_over":
                score, level, best = result[1], result[2], result[3]
                go_action = game_over_screen(SCREEN, font, score, level, best)
                if go_action == "quit":
                    break
                elif go_action == "menu":
                    continue
                elif go_action == "retry":
                    continue
        elif action == "leaderboard":
            leaderboard_screen(SCREEN, font, conn)
        elif action == "settings":
            back, new_settings = settings_screen(SCREEN, font, settings)
            if back == "back":
                settings = new_settings
                save_settings(settings)
        elif action == "quit":
            break
    
    conn.close()
    pygame.quit()


main()