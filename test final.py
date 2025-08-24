import asyncio
import platform
import pygame
import sys
import random
import math

# Intro screen using Pygame
async def show_intro_pygame():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chicken Invaders Clone 🚀")
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    CYAN = (0, 255, 255)
    font = pygame.font.SysFont("Arial", 48)
    start_time = pygame.time.get_ticks()
    duration = 3000  # 3 seconds
    while pygame.time.get_ticks() - start_time < duration:
        screen.fill(BLACK)
        pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2 - 50), 50)
        title_text = font.render("🚀 Chicken Invaders Clone 🚀", True, CYAN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        await asyncio.sleep(0.016)  # ~60 FPS
    pygame.quit()

# Main menu
async def main_menu():
    pygame.init()
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

# Main game loop
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

    # Player 1
    try:
        player1_img = pygame.image.load("player-red-1.png")
        player1_img = pygame.transform.scale(player1_img, (50, 50))
    except Exception:
        player1_img = pygame.Surface((50, 50))
        player1_img.fill(RED)
    player1_rect = player1_img.get_rect(center=(WIDTH // 4 if two_players else WIDTH // 2, HEIGHT - 50))
    player_speed = 8

    # Player 2
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
    powerup_speed = 3
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
    max_level = 3  # Levels 1-3, then boss

    # Boss setup
    boss = None
    boss_img = None
    boss_health = 100
    boss_bullets = []  # List of dictionaries containing position and velocity
    boss_bullet_speed = 5
    boss_bullet_timer = 0
    boss_bullet_interval = 60
    boss_movement_speed = 0.5  # Initial boss movement speed

    # Load the boss bullet image
    try:
        boss_bullet_img = pygame.image.load("egg.png")
        boss_bullet_img = pygame.transform.scale(boss_bullet_img, (40, 40))  # Adjust size as needed
    except Exception:
        boss_bullet_img = pygame.Surface((20, 20))
        boss_bullet_img.fill(RED)  # Fallback color if image fails to load

    # Load victory image
    try:
        victory_img = pygame.image.load("victory.png")
        victory_img = pygame.transform.scale(victory_img, (200, 200))  # Adjust size as needed
    except Exception:
        victory_img = pygame.Surface((200, 200))
        victory_img.fill((0, 255, 0))  # Green fallback

    clock = pygame.time.Clock()

    while level <= max_level + 1:
        # Level-specific settings
        if level == 1:
            enemy_speed = 2
            enemy_spawn_rate = 60
            powerup_spawn_rate = 300
            required_enemies = 1
        elif level == 2:
            enemy_speed = 3
            enemy_spawn_rate = 45
            powerup_spawn_rate = 360
            required_enemies = 1
        elif level == 3:
            enemy_speed = 4
            enemy_spawn_rate = 30
            powerup_spawn_rate = 420
            required_enemies = 1
        elif level == 4:  # Boss level
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
                    boss_img.fill((255, 0, 255))  # Magenta fallback
                boss = boss_img.get_rect(center=(WIDTH // 2, 100))
                boss_health = 100
                boss_bullet_timer = 0

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

            # Player 1 movement and shooting
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player1_rect.left > 0:
                player1_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player1_rect.right < WIDTH:
                player1_rect.x += player_speed
            if keys[pygame.K_SPACE] and bullet_cooldown1 <= 0:
                bullet = pygame.Rect(player1_rect.centerx - 2, player1_rect.top, 4, 10)
                bullets.append(bullet)
                bullet_cooldown1 = bullet_cooldown_max
            if bullet_cooldown1 > 0:
                bullet_cooldown1 -= 1

            # Player 2 movement and shooting
            if two_players:
                if keys[pygame.K_a] and player2_rect.left > 0:
                    player2_rect.x -= player_speed
                if keys[pygame.K_d] and player2_rect.right < WIDTH:
                    player2_rect.x += player_speed
                if keys[pygame.K_w] and bullet_cooldown2 <= 0:
                    bullet = pygame.Rect(player2_rect.centerx - 2, player2_rect.top, 4, 10)
                    bullets.append(bullet)
                    bullet_cooldown2 = bullet_cooldown_max
                if bullet_cooldown2 > 0:
                    bullet_cooldown2 -= 1

            # Update bullets
            for bullet in bullets[:]:
                bullet.y += bullet_speed
                if bullet.y < 0 or bullet.y > HEIGHT:
                    bullets.remove(bullet)

            # Spawn enemies
            if level <= max_level:
                enemy_spawn_timer += 1
                if enemy_spawn_timer >= enemy_spawn_rate:
                    enemy_rect = enemy_img.get_rect(center=(random.randint(100, WIDTH - 100), 0))
                    spawn_time = pygame.time.get_ticks() / 1000.0
                    x_offset = enemy_rect.centerx
                    enemies.append(enemy_rect)
                    enemy_data.append((enemy_rect, spawn_time, x_offset))
                    enemy_spawn_timer = 0

            # Update enemies
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

            # Spawn power-ups
            if level <= max_level:
                powerup_spawn_timer += 1
                if powerup_spawn_timer >= powerup_spawn_rate:
                    powerup_rect = powerup_img.get_rect(center=(random.randint(20, WIDTH - 20), 0))
                    powerups.append(powerup_rect)
                    powerup_spawn_timer = 0

            # Update power-ups
            for powerup in powerups[:]:
                powerup.y += powerup_speed
                if powerup.y > HEIGHT:
                    powerups.remove(powerup)
                if powerup.colliderect(player1_rect):
                    powerups.remove(powerup)
                    powerup_active1 = True
                    powerup_timer1 = powerup_duration
                    bullet_cooldown_max = 10
                if two_players and powerup.colliderect(player2_rect):
                    powerups.remove(powerup)
                    powerup_active2 = True
                    powerup_timer2 = powerup_duration
                    bullet_cooldown_max = 10

            # Update power-up effects
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

            # Update boss
            if level == 4 and boss:
                elapsed = pygame.time.get_ticks() / 1000.0
                boss.x = WIDTH // 2 + (WIDTH // 4) * math.sin(elapsed * boss_movement_speed)
                boss_bullet_timer += 1

                # Increase difficulty when boss health is below 50
                if boss_health <= 50:
                    boss_bullet_speed = 7  # Faster bullets
                    boss_bullet_interval = 40  # Faster bullet spawn rate
                    boss_movement_speed = 1.0  # Faster movement

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

                # Update boss bullets
                for bullet in boss_bullets[:]:
                    bullet["x"] += bullet["vx"]
                    bullet["y"] += bullet["vy"]

                    # Remove bullets that go off-screen
                    if bullet["y"] > HEIGHT or bullet["x"] < 0 or bullet["x"] > WIDTH:
                        boss_bullets.remove(bullet)

                    # Check for collisions with players
                    bullet_rect = pygame.Rect(bullet["x"], bullet["y"], boss_bullet_img.get_width(), boss_bullet_img.get_height())
                    if bullet_rect.colliderect(player1_rect) or (two_players and bullet_rect.colliderect(player2_rect)):
                        boss_bullets.remove(bullet)
                        lives -= 1
                        if lives <= 0:
                            running = False

            # Collision detection: player bullets vs enemies/boss
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
                    if boss_health <= 0:
                        running = False
                        level += 1
            for i in sorted(enemies_to_remove, reverse=True):
                enemies.pop(i)
                enemy_data.pop(i)

            # Collision detection: enemy vs players
            for enemy in enemies:
                if enemy.colliderect(player1_rect) or (two_players and enemy.colliderect(player2_rect)):
                    running = False
                    break

            # Check for level completion
            if level <= max_level and defeated_enemies >= required_enemies:
                screen.fill(BLACK)
                level_text = font.render(f"Level {level} Complete!", True, WHITE)
                screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2))
                pygame.display.update()
                await asyncio.sleep(2)
                level += 1
                enemies = []
                enemy_data = []
                powerups = []
                break

            # Update background
            bg_y = (bg_y + bg_speed) % HEIGHT
            screen.blit(background, (0, bg_y))
            screen.blit(background, (0, bg_y - HEIGHT))

            # Draw everything
            screen.blit(player1_img, player1_rect)
            if two_players and player2_img and player2_rect:
                screen.blit(player2_img, player2_rect)
            for bullet in bullets:
                pygame.draw.rect(screen, WHITE, bullet)
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

    # Game over or victory screen
    screen.fill(BLACK)
    if level > max_level + 1:
        screen.blit(victory_img, (WIDTH // 2 - victory_img.get_width() // 2, HEIGHT // 2 - victory_img.get_height() - 50))
        end_text = font.render(f"Victory! Score: {score}", True, WHITE)
    else:
        end_text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    await asyncio.sleep(2)

# Run the game
async def main():
    await show_intro_pygame()
    await main_menu()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())