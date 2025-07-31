import pygame
import random
import platform
import asyncio
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Bird properties
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5
FLAP = -10
BIRD_SIZE = 30

# Pipe properties
PIPE_WIDTH = 50
PIPE_GAP = 150
pipe_x = WIDTH
pipe_height = random.randint(150, 400)
PIPE_SPEED = 3

# Enemy properties
enemy_x = WIDTH
enemy_y = random.randint(50, HEIGHT - 50)
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 20
ENEMY_SPEED = 2
SHOOT_INTERVAL = 120  # Frames between shots
shoot_timer = 0
projectiles = []

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over = False

def setup():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, game_over, enemy_x, enemy_y, shoot_timer, projectiles
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(150, 400)
    enemy_x = WIDTH
    enemy_y = random.randint(50, HEIGHT - 50)
    shoot_timer = 0
    projectiles = []
    score = 0
    game_over = False

def draw_bird():
    pygame.draw.circle(screen, BLUE, (int(bird_x), int(bird_y)), BIRD_SIZE // 2)

def draw_pipes():
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_height))
    pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT))

def draw_enemy():
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT))

def draw_projectiles():
    for proj in projectiles:
        pygame.draw.circle(screen, YELLOW, (int(proj[0]), int(proj[1])), 5)

def shoot_projectile():
    # Calculate direction to bird
    dx = bird_x - (enemy_x + ENEMY_WIDTH / 2)
    dy = bird_y - (enemy_y + ENEMY_HEIGHT / 2)
    dist = math.hypot(dx, dy)
    if dist == 0:
        dist = 1
    dx, dy = dx / dist, dy / dist
    speed = 5
    return [enemy_x + ENEMY_WIDTH / 2, enemy_y + ENEMY_HEIGHT / 2, dx * speed, dy * speed]

def check_collision():
    bird_rect = pygame.Rect(bird_x - BIRD_SIZE // 2, bird_y - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
    pipe_top = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    pipe_bottom = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)
    
    if (bird_rect.colliderect(pipe_top) or bird_rect.colliderect(pipe_bottom) or 
        bird_rect.colliderect(enemy_rect) or bird_y < 0 or bird_y > HEIGHT):
        return True
    
    # Check projectile collisions with bird
    for proj in projectiles:
        proj_rect = pygame.Rect(proj[0] - 5, proj[1] - 5, 10, 10)
        if bird_rect.colliderect(proj_rect):
            return True
    
    return False

def check_projectile_pipe_collision(proj_x, proj_y):
    pipe_top = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    pipe_bottom = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    proj_rect = pygame.Rect(proj_x - 5, proj_y - 5, 10, 10)
    return proj_rect.colliderect(pipe_top) or proj_rect.colliderect(pipe_bottom)

def update_loop():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, game_over, enemy_x, enemy_y, shoot_timer, projectiles
    
    if not game_over:
        # Update bird
        bird_velocity += GRAVITY
        bird_y += bird_velocity
        
        # Update pipes
        pipe_x -= PIPE_SPEED
        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 400)
            score += 1
        
        # Update enemy
        enemy_x -= ENEMY_SPEED
        if enemy_x < -ENEMY_WIDTH:
            enemy_x = WIDTH
            enemy_y = random.randint(50, HEIGHT - 50)
        
        # Handle shooting
        shoot_timer += 1
        if shoot_timer >= SHOOT_INTERVAL:
            projectiles.append(shoot_projectile())
            shoot_timer = 0
        
        # Update projectiles
        new_projectiles = []
        for proj in projectiles:
            proj[0] += proj[2]
            proj[1] += proj[3]
            if 0 <= proj[0] <= WIDTH and 0 <= proj[1] <= HEIGHT:
                if not check_projectile_pipe_collision(proj[0], proj[1]):
                    new_projectiles.append(proj)
        projectiles[:] = new_projectiles
        
        # Check collision
        if check_collision():
            game_over = True
        
        # Draw everything
        screen.fill(WHITE)
        draw_pipes()
        draw_bird()
        draw_enemy()
        draw_projectiles()
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        
        pygame.display.flip()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = FLAP
            if event.key == pygame.K_r and game_over:
                setup()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / 60)  # 60 FPS

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
