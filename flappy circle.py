import pygame
import random
import platform
import asyncio

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Circle By Wyatt Stark")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Bird properties
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5
FLAP = -9
BIRD_SIZE = 20

# Pipe properties
PIPE_WIDTH = 50
PIPE_GAP = 150
pipe_x = WIDTH
pipe_height = random.randint(150, 400)
PIPE_SPEED = 3

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over = False

def setup():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(150, 400)
    score = 0
    game_over = False

def draw_bird():
    pygame.draw.circle(screen, BLUE, (int(bird_x), int(bird_y)), BIRD_SIZE // 2)

def draw_pipes():
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_height))
    pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT))

def check_collision():
    bird_rect = pygame.Rect(bird_x - BIRD_SIZE // 2, bird_y - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
    pipe_top = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
    pipe_bottom = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    
    if bird_rect.colliderect(pipe_top) or bird_rect.colliderect(pipe_bottom) or bird_y < 0 or bird_y > HEIGHT:
        return True
    return False

def update_loop():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, game_over
    
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
        
        # Check collision
        if check_collision():
            game_over = True
        
        # Draw everything
        screen.fill(WHITE)
        draw_pipes()
        draw_bird()
        
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
