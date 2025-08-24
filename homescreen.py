import pygame
import sys
import turtle
import time
import random
import math

# 1. Intro screen using Turtle (unchanged)
def show_intro_turtle():
    screen = turtle.Screen()
    screen.bgcolor("black")
    t = turtle.Turtle()
    t.color("white")
    t.hideturtle()
    t.speed(2)

    t.penup()
    t.goto(0, -50)
    t.pendown()
    t.begin_fill()
    t.circle(50)
    t.end_fill()

    t.penup()
    t.goto(0, 100)
    t.color("cyan")
    t.write("🚀 Chicken Invaders Clone 🚀", align="center", font=("Arial", 24, "bold"))

    time.sleep(3)
    turtle.bye()

# 2. Main menu using Pygame (slightly modified for title)
def main_menu():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chicken Invaders Clone 🚀")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 150, 255)

    font = pygame.font.SysFont("Arial", 48)
    button_font = pygame.font.SysFont("Arial", 36)

    # Load spaceship image (ensure it exists or handle error)
    try:
        spaceship_img = pygame.image.load("spaceship.jpg")
        spaceship_img = pygame.transform.scale(spaceship_img, (100, 100))
    except pygame.error:
        spaceship_img = pygame.Surface((100, 100))
        spaceship_img.fill(BLUE)  # Fallback if image missing

    image_y = 50
    image_height = spaceship_img.get_height()
    gap = 50
    text_y = image_y + image_height + gap

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        rect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, rect)

    while True:
        screen.fill(BLACK)

        screen.blit(spaceship_img, (WIDTH//2 - 50, image_y))
        draw_text("🚀 Chicken Invaders Clone 🚀", font, WHITE, screen, WIDTH//2, text_y)

        button_start_y = text_y + 100
        button_quit_y = button_start_y + 70

        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 100, button_start_y, 200, 50))
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 100, button_quit_y, 200, 50))

        draw_text("Start", button_font, WHITE, screen, WIDTH//2, button_start_y + 25)
        draw_text("Quit", button_font, WHITE, screen, WIDTH//2, button_quit_y + 25)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_start_y < mouse_y < button_start_y + 50 and WIDTH//2 - 100 < mouse_x < WIDTH//2 + 100:
                    game_loop(screen, WIDTH, HEIGHT)
                if button_quit_y < mouse_y < button_quit_y + 50 and WIDTH//2 - 100 < mouse_x < WIDTH//2 + 100:
                    pygame.quit()
                    sys.exit()

# 3. Main game loop
def game_loop(screen, WIDTH, HEIGHT):
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Fonts
    font = pygame.font.SysFont("Arial", 24)

    # Scrolling background
    try:
        background = pygame.image.load("background-blue.png")  # Space stars image
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except pygame.error:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(BLACK)
    bg_y = 0
    bg_speed = 1

    # Player setup
    try:
        player_img = pygame.image.load("player-red-1.png")
        player_img = pygame.transform.scale(player_img, (50, 50))
    except pygame.error:
        player_img = pygame.Surface((50, 50))
        player_img.fill(RED)
    player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT - 50))
    player_speed = 5

    # Bullet setup
    bullets = []
    bullet_speed = -10
    bullet_cooldown = 0
    bullet_cooldown_max = 20  # Default cooldown
    bullet_img = None  # Optional: Replace bullet rect with image
    # try:
    #     bullet_img = pygame.image.load("laser.png")
    #     bullet_img = pygame.transform.scale(bullet_img, (4, 10))
    # except pygame.error:
    #     bullet_img = None

    # Enemy setup (chickens with wavy movement)
    enemies = []
    enemy_speed = 2
    enemy_spawn_rate = 60
    enemy_spawn_timer = 0
    try:
        enemy_img = pygame.image.load("chicken.png")
        enemy_img = pygame.transform.scale(enemy_img, (30, 30))
    except pygame.error:
        enemy_img = pygame.Surface((30, 30))
        enemy_img.fill(WHITE)
    # Store enemy movement data
    enemy_data = []  # List of (rect, spawn_time, x_offset) for wavy motion

    # Power-up setup
    powerups = []
    powerup_spawn_rate = 300  # Every 5 seconds (60 FPS)
    powerup_spawn_timer = 0
    try:
        powerup_img = pygame.image.load("powerup.png      ")  # Gift box or similar
        powerup_img = pygame.transform.scale(powerup_img, (20, 20))
    except pygame.error:
        powerup_img = pygame.Surface((20, 20))
        powerup_img.fill((255, 255, 0))  # Yellow fallback
    powerup_speed = 3
    powerup_active = False
    powerup_timer = 0
    powerup_duration = 300  # 5 seconds at 60 FPS

    # Life setup (5 hearts)
    lives = 5
    try:
        heart_img = pygame.image.load("lives.webp")
        heart_img = pygame.transform.scale(heart_img, (30, 30))
    except pygame.error:
        heart_img = pygame.Surface((30, 30))
        heart_img.fill(RED)

    # Sound setup (placeholders; uncomment and add files)
    # pygame.mixer.init()
    # try:
    #     shoot_sound = pygame.mixer.Sound("laser.wav")
    #     hit_sound = pygame.mixer.Sound("explosion.wav")
    #     powerup_sound = pygame.mixer.Sound("powerup.wav")
    # except pygame.error:
    #     shoot_sound = hit_sound = powerup_sound = None

    # Score
    score = 0

    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        # Shooting
        if keys[pygame.K_SPACE] and bullet_cooldown <= 0:
            bullet = pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 10)
            bullets.append(bullet)
            bullet_cooldown = bullet_cooldown_max
            # if shoot_sound:
            #     shoot_sound.play()
        if bullet_cooldown > 0:
            bullet_cooldown -= 1

        # Update bullets
        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Spawn enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_rate:
            enemy_rect = enemy_img.get_rect(center=(random.randint(50, WIDTH-50), 0))
            spawn_time = time.time()
            x_offset = enemy_rect.centerx  # Base x for wavy motion
            enemies.append(enemy_rect)
            enemy_data.append((enemy_rect, spawn_time, x_offset))
            enemy_spawn_timer = 0

        # Update enemies (wavy movement)
        for i, (enemy, spawn_time, x_offset) in enumerate(enemy_data[:]):
            # Sinusoidal movement: x = offset + amplitude * sin(frequency * time)
            elapsed = time.time() - spawn_time
            enemy.y += enemy_speed
            enemy.x = x_offset + 50 * math.sin(2 * elapsed)  # Amplitude=50, freq=2
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                enemy_data.pop(i)
                lives -= 1
                if lives <= 0:
                    running = False
            enemy_data[i] = (enemy, spawn_time, x_offset)  # Update data

        # Spawn power-ups
        powerup_spawn_timer += 1
        if powerup_spawn_timer >= powerup_spawn_rate:
            powerup_rect = powerup_img.get_rect(center=(random.randint(20, WIDTH-20), 0))
            powerups.append(powerup_rect)
            powerup_spawn_timer = 0

        # Update power-ups
        for powerup in powerups[:]:
            powerup.y += powerup_speed
            if powerup.y > HEIGHT:
                powerups.remove(powerup)
            if powerup.colliderect(player_rect):
                powerups.remove(powerup)
                powerup_active = True
                powerup_timer = powerup_duration
                bullet_cooldown_max = 10  # Faster shooting
                # if powerup_sound:
                #     powerup_sound.play()

        # Update power-up effect
        if powerup_active:
            powerup_timer -= 1
            if powerup_timer <= 0:
                powerup_active = False
                bullet_cooldown_max = 20  # Revert to normal

        # Collision detection: bullet vs enemy
        for bullet in bullets[:]:
            for i, (enemy, _, _) in enumerate(enemy_data[:]):
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemy_data.pop(i)
                    score += 10
                    # if hit_sound:
                    #     hit_sound.play()
                    break

        # Collision detection: enemy vs player
        for enemy in enemies:
            if enemy.colliderect(player_rect):
                running = False
                break

        # Update background
        bg_y = (bg_y + bg_speed) % HEIGHT
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - HEIGHT))

        # Draw everything
        screen.blit(player_img, player_rect)
        for bullet in bullets:
            if bullet_img:
                screen.blit(bullet_img, bullet)
            else:
                pygame.draw.rect(screen, WHITE, bullet)
        for enemy in enemies:
            screen.blit(enemy_img, enemy)
        for powerup in powerups:
            screen.blit(powerup_img, powerup)

        # Draw hearts
        for i in range(lives):
            screen.blit(heart_img, (10 + i * 40, 50))

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.update()

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    time.sleep(2)
    return

# 4. Run the game
def run_game():
    show_intro_turtle()
    main_menu()

if __name__ == "__main__":
    run_game()