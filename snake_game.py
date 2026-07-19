import pygame
import random
import sys

# ---------------- Initialization ----------------
pygame.init()

# Screen settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Colors
BLACK = (15, 15, 15)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 140, 0)
RED = (220, 30, 30)
WHITE = (240, 240, 240)
GRAY = (40, 40, 40)

FONT = pygame.font.SysFont("consolas", 24)
BIG_FONT = pygame.font.SysFont("consolas", 48)

# Speed (frames per second) - increases slightly as score grows
BASE_SPEED = 8


def random_food_position(snake_body):
    """Pick a random grid cell that isn't occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake_body:
            return pos


def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_cell(pos, color):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def show_message(text, y_offset=0, font=BIG_FONT, color=WHITE):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)


def game_loop():
    # Snake starts in the middle, moving right
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    next_direction = direction

    food = random_food_position(snake)
    score = 0
    running = True
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        return game_loop()  # restart
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        next_direction = (1, 0)

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                game_over = True

            # Check self collision
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                else:
                    snake.pop()  # remove tail if no food eaten

        
        screen.fill(BLACK)
        draw_grid()
        draw_cell(food, RED)

        for i, segment in enumerate(snake):
            color = GREEN if i == 0 else DARK_GREEN
            draw_cell(segment, color)

        score_surface = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))

        if game_over:
            show_message("GAME OVER", y_offset=-20)
            show_message("Press R to Restart or Q to Quit", y_offset=30, font=FONT)

        pygame.display.flip()

        # Speed slightly increases with score, capped for playability
        speed = min(BASE_SPEED + score // 3, 20)
        clock.tick(speed)


if __name__ == "__main__":
    game_loop()
