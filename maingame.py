import asyncio
import platform
import pygame
import sys
import random
import math
import turtle
import time

# Turtle loading screen with "Loading" text
async def show_loading_screen():
    screen = turtle.Screen()
    screen.title("Loading...")
    screen.bgcolor("black")
    t = turtle.Turtle()
    t.speed(0)
    t.color("cyan")
    t.hideturtle()

    def draw_circle_midpoint(radius):
        def plot_point(x, y, center_x=0, center_y=0):
            for px, py in [
                (x, y), (x, -y), (-x, y), (-x, -y),
                (y, x), (y, -x), (-y, x), (-y, -x)
            ]:
                t.goto(center_x + px, center_y + py)
                t.pendown()
                t.dot(2)
                t.penup()

        x = radius
        y = 0
        p = 1 - radius
        plot_point(x, y)

        while x > y:
            y += 1
            if p <= 0:
                p += 2 * y + 3
            else:
                x -= 1
                p += 2 * (y - x) + 5
            plot_point(x, y)

    try:
        turtle.tracer(0)
        draw_circle_midpoint(100)
        t.penup()
        t.goto(0, -20)
        t.write("Loading", align="center", font=("Arial", 24, "bold"))
        turtle.tracer(1)
        start_time = time.time()
        while time.time() - start_time < 3:
            await asyncio.sleep(0.1)
    finally:
        turtle.bye()

# Intro screen using Pygame with Midpoint Circle
async def show_intro_pygame():
    pygame.init()
    pygame.mixer.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chicken Invaders Clone 🚀")
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    CYAN = (0, 255, 255)
    font = pygame.font.SysFont("Arial", 48)
    start_time = pygame.time.get_ticks()
    duration = 3000  # 3 seconds

    def draw_circle_midpoint_pygame(screen, center_x, center_y, radius, color):
        def plot_point(x, y):
            for px, py in [
                (x, y), (x, -y), (-x, y), (-x, -y),
                (y, x), (y, -x), (-y, x), (-y, -x)
            ]:
                if 0 <= center_x + px < WIDTH and 0 <= center_y + py < HEIGHT:
                    screen.set_at((center_x + px, center_y + py), color)

        x = radius
        y = 0
        p = 1 - radius

        plot_point(x, y)

        while x > y:
            y += 1
            if p <= 0:
                p += 2 * y + 3
            else:
                x -= 1
                p += 2 * (y - x) + 5
            plot_point(x, y)

    while pygame.time.get_ticks() - start_time < duration:
        screen.fill(BLACK)
        draw_circle_midpoint_pygame(screen, WIDTH // 2, HEIGHT // 2 - 50, 50, WHITE)
        title_text = font.render("🚀 Chicken Invaders Clone 🚀", True, CYAN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        await asyncio.sleep(0.016)  # ~60 FPS
    pygame.quit()

# Main menu (unchanged)
async def main_menu():
    pygame.init()
    pygame.mixer.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chicken Invaders Clone 🚀")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 150, 255)
    CYAN = (0, 255, 255)
    font = pygame.font.SysFont("Arial", 48)
    button_font = pygame.font.SysFont("Arial", 36)
    try:
        spaceship_img = pygame.image.load("spaceship.jpg")
        spaceship_img = pygame.transform.scale(spaceship_img, (100, 100))
    except Exception:
        spaceship_img = pygame.Surface((100, 100))
        spaceship_img.fill(BLUE)
    image_y = 50
    gap = 50
    text_y = image_y + spaceship_img.get_height() + gap

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        rect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, rect)

    two_players = False
    while True:
        screen.fill(BLACK)
        screen.blit(spaceship_img, (WIDTH // 2 - 50, image_y))
        draw_text("🚀 Chicken Invaders Clone 🚀", font, WHITE, screen, WIDTH // 2, text_y)
        button_start_y = text_y + 100
        button_two_players_y = button_start_y + 70
        button_quit_y = button_two_players_y + 70
        pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, button_start_y, 200, 50))
        pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, button_two_players_y, 200, 50))
        pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 100, button_quit_y, 200, 50))
        draw_text("Start", button_font, WHITE, screen, WIDTH // 2, button_start_y + 25)
        draw_text("2 Players", button_font, CYAN if two_players else WHITE, screen, WIDTH // 2, button_two_players_y + 25)
        draw_text("Quit", button_font, WHITE, screen, WIDTH // 2, button_quit_y + 25)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_start_y < mouse_y < button_start_y + 50 and WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100:
                    await game_loop(screen, WIDTH, HEIGHT, two_players)
                if button_two_players_y < mouse_y < button_two_players_y + 50 and WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100:
                    two_players = not two_players
                    draw_text("2 Players", button_font, CYAN if two_players else WHITE, screen, WIDTH // 2, button_two_players_y + 25)
                    pygame.display.update()
                if button_quit_y < mouse_y < button_quit_y + 50 and WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100:
                    pygame.quit()
                    sys.exit()

# DDA Line Algorithm
def draw_line_dda(screen, x0, y0, x1, y1, color):
    # Calculate differences
    dx = x1 - x0
    dy = y1 - y0
    
    # Determine steps and increment
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        if 0 <= x0 < screen.get_width() and 0 <= y0 < screen.get_height():
            screen.set_at((int(x0), int(y0)), color)
        return

    x_increment = dx / steps
    y_increment = dy / steps

    # Initialize starting point
    x = x0
    y = y0

    # Draw pixels
    for _ in range(int(steps) + 1):
        if 0 <= int(x) < screen.get_width() and 0 <= int(y) < screen.get_height():
            screen.set_at((int(x), int(y)), color)
        x += x_increment
        y += y_increment

# Main game loop with DDA lines
async def game_loop(screen, WIDTH, HEIGHT, two_players):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    font = pygame.font.SysFont("Arial", 24)
    try:
        background = pygame.image.load("background.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except Exception:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(BLACK)
    bg_y = 0
    bg_speed = 1

    try:
        player1_img = pygame.image.load("player-red-1.png")
        player1_img = pygame.transform.scale(player1_img, (50, 50))
    except Exception:
        player1_img = pygame.Surface((50, 50))
        player1_img.fill(RED)
    player1_rect = player1_img.get_rect(center=(WIDTH // 4 if two_players else WIDTH // 2, HEIGHT - 50))
    player_speed = 8

    player2_rect = None
    player2_img = None
    if two_players:
        try:
            player2_img = pygame.image.load("player-blue-1.png")
            player2_img = pygame.transform.scale(player2_img, (50, 50))
        except Exception:
            player2_img = pygame.Surface((50, 50))
            player2_img.fill(BLUE)
        player2_rect = player2_img.get_rect(center=(3 * WIDTH // 4, HEIGHT - 50))

    bullets = []
    bullet_speed = -10
    bullet_cooldown1 = 0
    bullet_cooldown2 = 0
    bullet_cooldown_max = 20

    try:
        bullet_img = pygame.image.load("laser.png")
        bullet_img = pygame.transform.scale(bullet_img, (10, 20))
    except Exception:
        bullet_img = pygame.Surface((4, 10))
        bullet_img.fill(WHITE)

    enemies = []
    enemy_data = []
    try:
        enemy_img = pygame.image.load("chicken.png")
        enemy_img = pygame.transform.scale(enemy_img, (30, 30))
    except Exception:
        enemy_img = pygame.Surface((30, 30))
        enemy_img.fill(WHITE)

    powerups = []
    try:
        powerup_img = pygame.image.load("powerup.png")
        powerup_img = pygame.transform.scale(powerup_img, (20, 20))
    except Exception:
        powerup_img = pygame.Surface((20, 20))
        powerup_img.fill((255, 255, 0))
    powerup_speed = 1.5
    powerup_active1 = False
    powerup_active2 = False
    powerup_timer1 = 0
    powerup_timer2 = 0
    powerup_duration = 300

    lives = 5
    try:
        heart_img = pygame.image.load("lives.webp")
        heart_img = pygame.transform.scale(heart_img, (30, 30))
    except Exception:
        heart_img = pygame.Surface((30, 30))
        heart_img.fill(RED)

    score = 0
    level = 1
    max_level = 3

    try:
        laser_sound = pygame.mixer.Sound("sfx-laser1.ogg")
        laser_sound.set_volume(0.5)
    except Exception:
        laser_sound = None
    try:
        powerup_sound = pygame.mixer.Sound("bite.mp3")
        powerup_sound.set_volume(0.5)
    except Exception:
        powerup_sound = None
    try:
        boss_defeat_sound = pygame.mixer.Sound("destroy.mp3")
        boss_defeat_sound.set_volume(0.7)
    except Exception:
        boss_defeat_sound = None

    pygame.mixer.set_num_channels(8)

    boss = None
    boss_img = None
    boss_health = 100
    boss_bullets = []
    boss_bullet_speed = 5
    boss_bullet_timer = 0
    boss_bullet_interval = 60
    boss_movement_speed = 0.5
    last_powerup_health = 100

    try:
        boss_bullet_img = pygame.image.load("egg.png")
        boss_bullet_img = pygame.transform.scale(boss_bullet_img, (40, 40))
    except Exception:
        boss_bullet_img = pygame.Surface((20, 20))
        boss_bullet_img.fill(RED)

    try:
        victory_img = pygame.image.load("victory.png")
        victory_img = pygame.transform.scale(victory_img, (200, 200))
    except Exception:
        victory_img = pygame.Surface((200, 200))
        victory_img.fill((0, 255, 0))

    clock = pygame.time.Clock()

    while level <= max_level + 1:
        if level == 1:
            enemy_speed = 2
            enemy_spawn_rate = 60
            powerup_spawn_rate = 600  # Increased from 300
            required_enemies = 8
        elif level == 2:
            enemy_speed = 3
            enemy_spawn_rate = 45
            powerup_spawn_rate = 720  # Increased from 360
            required_enemies = 10
        elif level == 3:
            enemy_speed = 4
            enemy_spawn_rate = 30
            powerup_spawn_rate = 840  # Increased from 420
            required_enemies = 13
        elif level == 4:
            enemy_speed = 0
            enemy_spawn_rate = float('inf')
            powerup_spawn_rate = float('inf')
            required_enemies = 0
            if not boss:
                try:
                    boss_img = pygame.image.load("chicken.png")
                    boss_img = pygame.transform.scale(boss_img, (100, 100))
                except Exception:
                    boss_img = pygame.Surface((100, 100))
                    boss_img.fill((255, 0, 255))
                boss = boss_img.get_rect(center=(WIDTH // 2, 100))
                boss_health = 100
                boss_bullet_timer = 0
                last_powerup_health = 100

        enemy_spawn_timer = 0
        powerup_spawn_timer = 0
        defeated_enemies = 0
        running = True

        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player1_rect.left > 0:
                player1_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player1_rect.right < WIDTH:
                player1_rect.x += player_speed
            if keys[pygame.K_SPACE] and bullet_cooldown1 <= 0:
                bullet = bullet_img.get_rect(center=(player1_rect.centerx, player1_rect.top))
                bullets.append(bullet)
                bullet_cooldown1 = bullet_cooldown_max
                if laser_sound:
                    laser_sound.play()
            if bullet_cooldown1 > 0:
                bullet_cooldown1 -= 1

            if two_players:
                if keys[pygame.K_a] and player2_rect.left > 0:
                    player2_rect.x -= player_speed
                if keys[pygame.K_d] and player2_rect.right < WIDTH:
                    player2_rect.x += player_speed
                if keys[pygame.K_w] and bullet_cooldown2 <= 0:
                    bullet = bullet_img.get_rect(center=(player2_rect.centerx, player2_rect.top))
                    bullets.append(bullet)
                    bullet_cooldown2 = bullet_cooldown_max
                    if laser_sound:
                        laser_sound.play()
                if bullet_cooldown2 > 0:
                    bullet_cooldown2 -= 1

            for bullet in bullets[:]:
                bullet.y += bullet_speed
                if bullet.y < 0 or bullet.y > HEIGHT:
                    bullets.remove(bullet)

            if level <= max_level:
                enemy_spawn_timer += 1
                if enemy_spawn_timer >= enemy_spawn_rate:
                    enemy_rect = enemy_img.get_rect(center=(random.randint(100, WIDTH - 100), 0))
                    spawn_time = pygame.time.get_ticks() / 1000.0
                    x_offset = enemy_rect.centerx
                    enemies.append(enemy_rect)
                    enemy_data.append((enemy_rect, spawn_time, x_offset))
                    enemy_spawn_timer = 0

            enemies_to_remove = []
            for i, (enemy, spawn_time, x_offset) in enumerate(enemy_data):
                elapsed = pygame.time.get_ticks() / 1000.0 - spawn_time
                enemy.y += enemy_speed
                enemy.x = x_offset + 50 * math.sin(2 * elapsed)
                if enemy.y > HEIGHT:
                    enemies_to_remove.append(i)
                    lives -= 1
                    if lives <= 0:
                        running = False
                else:
                    enemy_data[i] = (enemy, spawn_time, x_offset)
            for i in sorted(enemies_to_remove, reverse=True):
                enemies.pop(i)
                enemy_data.pop(i)

            if level <= max_level:
                powerup_spawn_timer += 1
                if powerup_spawn_timer >= powerup_spawn_rate:
                    powerup_rect = powerup_img.get_rect(center=(random.randint(20, WIDTH - 20), 0))
                    powerups.append(powerup_rect)
                    powerup_spawn_timer = random.randint(powerup_spawn_rate // 2, powerup_spawn_rate * 3 // 2)

            for powerup in powerups[:]:
                powerup.y += powerup_speed
                if powerup.y > HEIGHT:
                    powerups.remove(powerup)
                if powerup.colliderect(player1_rect):
                    powerups.remove(powerup)
                    powerup_active1 = True
                    powerup_timer1 = powerup_duration
                    bullet_cooldown_max = 10
                    if powerup_sound:
                        powerup_sound.play()
                if two_players and powerup.colliderect(player2_rect):
                    powerups.remove(powerup)
                    powerup_active2 = True
                    powerup_timer2 = powerup_duration
                    bullet_cooldown_max = 10
                    if powerup_sound:
                        powerup_sound.play()

            if powerup_active1:
                powerup_timer1 -= 1
                if powerup_timer1 <= 0:
                    powerup_active1 = False
                    bullet_cooldown_max = 20
            if powerup_active2:
                powerup_timer2 -= 1
                if powerup_timer2 <= 0:
                    powerup_active2 = False
                    bullet_cooldown_max = 20

            if level == 4 and boss:
                elapsed = pygame.time.get_ticks() / 1000.0
                boss.x = WIDTH // 2 + (WIDTH // 4) * math.sin(elapsed * boss_movement_speed)
                boss_bullet_timer += 1

                if boss_health <= 50:
                    boss_bullet_speed = 7
                    boss_bullet_interval = 40
                    boss_movement_speed = 1.0

                if boss_bullet_timer >= boss_bullet_interval:
                    for angle in [-30, 0, 30]:
                        bullet = {
                            "x": boss.centerx - boss_bullet_img.get_width() // 2,
                            "y": boss.bottom,
                            "vx": math.sin(math.radians(angle)) * boss_bullet_speed,
                            "vy": boss_bullet_speed
                        }
                        boss_bullets.append(bullet)
                    boss_bullet_timer = 0

                for bullet in boss_bullets[:]:
                    bullet["x"] += bullet["vx"]
                    bullet["y"] += bullet["vy"]

                    if bullet["y"] > HEIGHT or bullet["x"] < 0 or bullet["x"] > WIDTH:
                        boss_bullets.remove(bullet)

                    bullet_rect = pygame.Rect(bullet["x"], bullet["y"], boss_bullet_img.get_width(), boss_bullet_img.get_height())
                    if bullet_rect.colliderect(player1_rect) or (two_players and bullet_rect.colliderect(player2_rect)):
                        boss_bullets.remove(bullet)
                        lives -= 1
                        if lives <= 0:
                            running = False

            enemies_to_remove = []
            for bullet in bullets[:]:
                hit = False
                for i, (enemy, _, _) in enumerate(enemy_data):
                    if bullet.colliderect(enemy):
                        enemies_to_remove.append(i)
                        bullets.remove(bullet)
                        score += 10
                        defeated_enemies += 1
                        hit = True
                        break
                if hit:
                    continue
                if level == 4 and boss and bullet.colliderect(boss):
                    bullets.remove(bullet)
                    boss_health -= 1
                    score += 20
                    if (last_powerup_health - boss_health) >= 20:
                        num_powerups = 2 if two_players else 1
                        for _ in range(num_powerups):
                            powerup_rect = powerup_img.get_rect(center=(random.randint(20, WIDTH - 20), boss.bottom))
                            powerups.append(powerup_rect)
                        last_powerup_health = boss_health
                    if boss_health <= 0:
                        if boss_defeat_sound:
                            boss_defeat_sound.play()
                        running = False
                        level += 1
            for i in sorted(enemies_to_remove, reverse=True):
                enemies.pop(i)
                enemy_data.pop(i)

            for enemy in enemies:
                if enemy.colliderect(player1_rect) or (two_players and enemy.colliderect(player2_rect)):
                    running = False
                    break

            if level <= max_level and defeated_enemies >= required_enemies:
                screen.fill(BLACK)
                level_text = font.render(f"Level {level} Complete!", True, WHITE)
                score_text = font.render(f"Score: {score}", True, WHITE)
                screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 30))
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
                # Draw DDA line under "Score"
                score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
                line_y = score_rect.bottom + 15
                line_x_start = score_rect.left - 10
                line_x_end = score_rect.right + 10
                draw_line_dda(screen, line_x_start, line_y, line_x_end, line_y, WHITE)
                pygame.display.update()
                await asyncio.sleep(2)
                level += 1
                enemies = []
                enemy_data = []
                powerups = []
                break

            bg_y = (bg_y + bg_speed) % HEIGHT
            screen.blit(background, (0, bg_y))
            screen.blit(background, (0, bg_y - HEIGHT))

            screen.blit(player1_img, player1_rect)
            if two_players and player2_img and player2_rect:
                screen.blit(player2_img, player2_rect)
            for bullet in bullets:
                screen.blit(bullet_img, bullet)
            for enemy in enemies:
                screen.blit(enemy_img, enemy)
            for powerup in powerups:
                screen.blit(powerup_img, powerup)
            if level == 4 and boss:
                screen.blit(boss_img, boss)
                for bullet in boss_bullets:
                    screen.blit(boss_bullet_img, (bullet["x"], bullet["y"]))
                health_text = font.render(f"Boss HP: {boss_health}", True, WHITE)
                screen.blit(health_text, (WIDTH - 150, 10))
            for i in range(lives):
                screen.blit(heart_img, (10 + i * 40, 50))
            score_text = font.render(f"Score: {score}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 30))
            pygame.display.update()
            await asyncio.sleep(0.016)

        if not running or level > max_level + 1:
            break

    screen.fill(BLACK)
    if level > max_level + 1:
        screen.blit(victory_img, (WIDTH // 2 - victory_img.get_width() // 2, HEIGHT // 2 - victory_img.get_height() - 50))
        end_text = font.render(f"Victory! Score: {score}", True, WHITE)
    else:
        end_text = font.render(f"Game Over! Score: {score}", True, WHITE)
    end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(end_text, end_rect)
    # Draw DDA line under "Game Over" or "Victory"
    line_y = end_rect.bottom + 15
    line_x_start = end_rect.left - 10
    line_x_end = end_rect.right + 10
    draw_line_dda(screen, line_x_start, line_y, line_x_end, line_y, WHITE)
    pygame.display.update()
    await asyncio.sleep(2)

    await show_loading_screen()

# Run the game
async def main():
    await show_intro_pygame()
    await main_menu()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())