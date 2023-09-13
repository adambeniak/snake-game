import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
DARK_GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = (0, -1)
snake_speed = 10

food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

playing = False
score = 0
top_score = 0

def load_top_score():
    try:
        with open("top_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_top_score():
    with open("top_score.txt", "w") as file:
        file.write(str(top_score))

top_score = load_top_score()

def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Skóre: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def show_menu():
    global playing, score, top_score
    menu_font = pygame.font.Font(None, 48)
    play_text = menu_font.render("Hrát", True, DARK_GREEN)
    quit_text = menu_font.render("Odejít", True, RED)
    retry_text = menu_font.render("Restartovat", True, DARK_GREEN)
    message_text = menu_font.render("Pokazil jsi to!", True, RED)
    top_score_text = menu_font.render(f"Top Skóre: {top_score}", True, BLACK)

    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    top_score_rect = top_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 65))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    start_game()
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                elif retry_rect.collidepoint(event.pos):
                    start_game()
                    return

        screen.fill(WHITE)

        if score > top_score:
            top_score = score
            save_top_score()

        screen.blit(message_text, message_rect)
        screen.blit(top_score_text, top_score_rect)
        if not playing:
            screen.blit(retry_text, retry_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

def start_game():
    global snake, snake_direction, food, playing, score
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (0, -1)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    playing = True
    score = 0

def update_game():
    global snake, snake_direction, food, playing, score
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_direction != (0, 1):
        snake_direction = (0, -1)
    if keys[pygame.K_DOWN] and snake_direction != (0, -1):
        snake_direction = (0, 1)
    if keys[pygame.K_LEFT] and snake_direction != (1, 0):
        snake_direction = (-1, 0)
    if keys[pygame.K_RIGHT] and snake_direction != (-1, 0):
        snake_direction = (1, 0)

    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

    if (
        new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
    ):
        playing = False
        show_menu()
        return

    snake.insert(0, new_head)

    if new_head in snake[1:]:
        playing = False
        show_menu()
        return

    if snake[0] == food:
        score += 1
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    else:
        snake.pop()

    screen.fill(WHITE)

    for segment in snake:
        pygame.draw.rect(
            screen, DARK_GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

    pygame.draw.rect(
        screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )

    display_score()
    pygame.display.flip()

    pygame.time.delay(1000 // snake_speed)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if playing:
        if keys[pygame.K_UP] and snake_direction != (0, 1):
            snake_direction = (0, -1)
        if keys[pygame.K_DOWN] and snake_direction != (0, -1):
            snake_direction = (0, 1)
        if keys[pygame.K_LEFT] and snake_direction != (1, 0):
            snake_direction = (-1, 0)
        if keys[pygame.K_RIGHT] and snake_direction != (-1, 0):
            snake_direction = (1, 0)

    if not playing and keys[pygame.K_SPACE]:
        start_game()

    if playing:
        update_game()
    else:
        show_menu()
