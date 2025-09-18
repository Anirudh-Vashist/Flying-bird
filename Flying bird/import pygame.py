import pygame
import random

# Initialize Pygame
pygame.init()

# Fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Flappy Bird")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game variables (same as before)
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.004
jump_strength = -0.6
pipe_speed = 1
pipe_gap = 160
pipe_frequency = 1800
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0

# Bird properties
bird_width = 50
bird_height = 50
bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

# Load bird image
bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))

# Load background image (pixel sky with clouds)
bg_img = pygame.image.load("background.png").convert()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Pipes list: [(rect, is_bottom, scored)]
pipes = []

# Game states: "intro", "play", "game_over"
game_state = "intro"


def draw_bird():
    screen.blit(bird_img, (bird_rect.x, bird_rect.y))


def create_pipe():
    pipe_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
    bottom_pipe_rect = pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap, 80, SCREEN_HEIGHT - pipe_height - pipe_gap)
    top_pipe_rect = pygame.Rect(SCREEN_WIDTH, 0, 80, pipe_height)
    return [(top_pipe_rect, False, False), (bottom_pipe_rect, True, False)]


def move_pipes():
    global pipes
    new_pipes = []
    for rect, is_bottom, scored in pipes:
        rect.x -= pipe_speed
        if rect.right > 0:
            new_pipes.append((rect, is_bottom, scored))
    pipes = new_pipes


def draw_pipes():
    for rect, _, _ in pipes:
        pygame.draw.rect(screen, GREEN, rect)


def check_collision():
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    for rect, _, _ in pipes:
        if bird_rect.colliderect(rect):
            return True
    return False


def display_score():
    font = pygame.font.SysFont("Arial", 40)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))


def reset_game():
    global bird_y, bird_velocity, pipes, score, last_pipe, bird_rect
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    score = 0
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    bird_rect.y = bird_y


# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "intro":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "play"

            elif game_state == "play":
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength

            elif game_state == "game_over":
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "play"

            if event.key == pygame.K_ESCAPE:  # Quit with ESC
                running = False

    # Draw background
    screen.blit(bg_img, (0, 0))

    if game_state == "intro":
        font = pygame.font.SysFont("Arial", 70)
        title_text = font.render("Flappy Bird", True, BLACK)
        start_text = font.render("Press Enter to Start", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

    elif game_state == "play":
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect.y = bird_y

        # Pipe creation
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipes.extend(create_pipe())
            last_pipe = time_now

        # Move and draw pipes
        move_pipes()
        draw_pipes()

        # Scoring
        for i in range(len(pipes)):
            rect, is_bottom, scored = pipes[i]
            if is_bottom and not scored and rect.right < bird_rect.left:
                score += 1
                pipes[i] = (rect, is_bottom, True)

        # Collision
        if check_collision():
            game_state = "game_over"

        draw_bird()
        display_score()

    elif game_state == "game_over":
        font = pygame.font.SysFont("Arial", 70)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        restart_text = font.render("Press Space to Restart", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))

    pygame.display.flip()

pygame.quit()
