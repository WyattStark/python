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
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Bird properties
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5
FLAP = -10
BIRD_SIZE = 30
MAX_HEALTH = 6
health = MAX_HEALTH
bird_projectiles = []
BIRD_SHOOT_INTERVAL = 30  # Frames between shots (0.5 seconds at 60 FPS)
bird_shoot_timer = 0
AMMO_CAPACITY = 10
ammo = AMMO_CAPACITY
RELOAD_TIME = 120  # Frames for reload (2 seconds at 60 FPS)
reload_timer = 0
is_reloading = False

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
SHOOT_INTERVAL = 120  # Frames between enemy shots
shoot_timer = 0
projectiles = []

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over = False
game_won = False
WIN_SCORE = 100
last_frame_time = pygame.time.get_ticks()
fps = 0

def setup():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, game_over, game_won, enemy_x, enemy_y, shoot_timer, projectiles, health, last_frame_time, fps, bird_projectiles, bird_shoot_timer, ammo, reload_timer, is_reloading
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(150, 400)
    enemy_x = WIDTH
    enemy_y = random.randint(50, HEIGHT - 50)
    shoot_timer = 0
    projectiles = []
    bird_projectiles = []
    bird_shoot_timer = 0
    score = 0
    health = MAX_HEALTH
    game_over = False
    game_won = False
    last_frame_time = pygame.time.get_ticks()
    fps = 0
    ammo = AMMO_CAPACITY
    reload_timer = 0
    is_reloading = False

def draw_bird():
    # Draw bird: oval body, triangular wing, small eye, gun
    body_rect = pygame.Rect(bird_x - BIRD_SIZE // 2, bird_y - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE // 1.5)
    pygame.draw.ellipse(screen, BLUE, body_rect)  # Oval body
    wing_points = [(bird_x - BIRD_SIZE // 2, bird_y), 
                   (bird_x - BIRD_SIZE, bird_y + BIRD_SIZE // 2), 
                   (bird_x - BIRD_SIZE // 2, bird_y + BIRD_SIZE // 2)]
    pygame.draw.polygon(screen, BLUE, wing_points)  # Left wing
    pygame.draw.circle(screen, BLACK, (bird_x + BIRD_SIZE // 4, bird_y - BIRD_SIZE // 4), 3)  # Eye
    gun_rect = pygame.Rect(bird_x + BIRD_SIZE // 2, bird_y - 5, 10, 5)  # Small gun on right
    pygame.draw.rect(screen, BLACK, gun_rect)

def draw_pipes():
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_height))
    pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT))

def draw_enemy():
    # Draw enemy: triangular spaceship with thruster
    body_points = [(enemy_x, enemy_y + ENEMY_HEIGHT // 2),
                   (enemy_x + ENEMY_WIDTH, enemy_y),
                   (enemy_x + ENEMY_WIDTH, enemy_y + ENEMY_HEIGHT)]
    pygame.draw.polygon(screen, RED, body_points)  # Triangular body
    thruster_rect = pygame.Rect(enemy_x - 10, enemy_y + ENEMY_HEIGHT // 4, 10, ENEMY_HEIGHT // 2)
    pygame.draw.rect(screen, GRAY, thruster_rect)  # Thruster
    cockpit_rect = pygame.Rect(enemy_x + ENEMY_WIDTH - 10, enemy_y + ENEMY_HEIGHT // 4, 5, ENEMY_HEIGHT // 2)
    pygame.draw.rect(screen, YELLOW, cockpit_rect)  # Cockpit detail

def draw_projectiles():
    # Draw enemy projectiles (yellow)
    for proj in projectiles:
        pygame.draw.circle(screen, YELLOW, (int(proj[0]), int(proj[1])), 5)
    # Draw bird projectiles (blue)
    for proj in bird_projectiles:
        pygame.draw.circle(screen, BLUE, (int(proj[0]), int(proj[1])), 5)

def draw_health_bar():
    # Draw health bar outline
    pygame.draw.rect(screen, BLACK, (WIDTH - 110, 50, 100, 20), 2)
    # Draw filled health bar
    health_width = (health / MAX_HEALTH) * 96
    pygame.draw.rect(screen, RED, (WIDTH - 108, 52, health_width, 16))

def draw_fps():
    # Draw FPS counter above health bar
    fps_text = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (WIDTH - 100, 10))

def draw_reload_message():
    if is_reloading:
        reload_text = font.render("Reloading...", True, (255, 0, 0))
        screen.blit(reload_text, (WIDTH // 2 - 80, HEIGHT - 50))

def shoot_bird_projectile():
    # Shoot straight right
    speed = 7
    return [bird_x + BIRD_SIZE // 2, bird_y, speed, 0]

def shoot_enemy_projectile():
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
    global health
    bird_rect = pygame.Rect(bird_x - BIRD_SIZE // 2, bird_y - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
    pipe_top = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    pipe_bottom = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)
    
    # Check pipe collision
    if bird_rect.colliderect(pipe_top) or bird_rect.colliderect(pipe_bottom):
        health -= 2
        if health <= 0:
            return True
    
    # Check enemy collision
    if bird_rect.colliderect(enemy_rect):
        health = 0
        return True
    
    # Check enemy projectile collisions with bird
    for proj in projectiles:
        proj_rect = pygame.Rect(proj[0] - 5, proj[1] - 5, 10, 10)
        if bird_rect.colliderect(proj_rect):
            health -= 3
            projectiles.remove(proj)  # Remove projectile on hit
            if health <= 0:
                return True
    
    # Check if bird is out of bounds
    if bird_y < 0 or bird_y > HEIGHT:
        health = 0
        return True
    
    return False

def check_projectile_pipe_collision(proj_x, proj_y):
    pipe_top = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    pipe_bottom = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    proj_rect = pygame.Rect(proj_x - 5, proj_y - 5, 10, 10)
    return proj_rect.colliderect(pipe_top) or proj_rect.colliderect(pipe_bottom)

def update_loop():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, game_over, game_won, enemy_x, enemy_y, shoot_timer, projectiles, health, last_frame_time, fps, bird_projectiles, bird_shoot_timer, ammo, reload_timer, is_reloading
    
    if not game_over and not game_won:
        # Calculate FPS
        current_time = pygame.time.get_ticks()
        frame_time = (current_time - last_frame_time) / 1000.0  # Convert to seconds
        if frame_time > 0:
            fps = 1.0 / frame_time
        last_frame_time = current_time
        
        # Update bird
        bird_velocity += GRAVITY
        bird_y += bird_velocity
        
        # Update pipes
        pipe_x -= PIPE_SPEED
        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 400)
            score += 1
        
        # Check win condition
        if score >= WIN_SCORE:
            game_won = True
        
        # Update enemy
        enemy_x -= ENEMY_SPEED
        if enemy_x < -ENEMY_WIDTH:
            enemy_x = WIDTH
            enemy_y = random.randint(50, HEIGHT - 50)
        
        # Handle enemy shooting
        shoot_timer += 1
        if shoot_timer >= SHOOT_INTERVAL:
            projectiles.append(shoot_enemy_projectile())
            shoot_timer = 0
        
        # Handle bird shooting timer
        bird_shoot_timer += 1
        
        # Handle reloading
        if is_reloading:
            reload_timer += 1
            if reload_timer >= RELOAD_TIME:
                is_reloading = False
                ammo = AMMO_CAPACITY
                reload_timer = 0
        
        # Update enemy projectiles
        new_projectiles = []
        for proj in projectiles:
            proj[0] += proj[2]
            proj[1] += proj[3]
            if 0 <= proj[0] <= WIDTH and 0 <= proj[1] <= HEIGHT:
                if not check_projectile_pipe_collision(proj[0], proj[1]):
                    new_projectiles.append(proj)
        projectiles[:] = new_projectiles
        
        # Update bird projectiles
        new_bird_projectiles = []
        for proj in bird_projectiles:
            proj[0] += proj[2]
            proj[1] += proj[3]
            if 0 <= proj[0] <= WIDTH and 0 <= proj[1] <= HEIGHT:
                if not check_projectile_pipe_collision(proj[0], proj[1]):
                    new_bird_projectiles.append(proj)
        bird_projectiles[:] = new_bird_projectiles
        
        # Check collision
        if check_collision():
            game_over = True
        
        # Draw everything
        screen.fill(WHITE)
        draw_pipes()
        draw_bird()
        draw_enemy()
        draw_projectiles()
        draw_health_bar()
        draw_fps()
        draw_reload_message()
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        
        if game_won:
            victory_text = font.render("Thanks for playing - Wyatt Stark", True, (0, 0, 255))
            screen.blit(victory_text, (WIDTH // 2 - 150, HEIGHT // 2))
        
        pygame.display.flip()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not game_won:
                bird_velocity = FLAP
            if event.key == pygame.K_r and (game_over or game_won):
                setup()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not game_won:
            if event.button == 1 and not is_reloading and ammo > 0 and bird_shoot_timer >= BIRD_SHOOT_INTERVAL:  # Left mouse button
                bird_projectiles.append(shoot_bird_projectile())
                ammo -= 1
                bird_shoot_timer = 0
            if event.button == 3 and ammo < AMMO_CAPACITY and not is_reloading:  # Right mouse button
                is_reloading = True
                reload_timer = 0

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
