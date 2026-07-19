import pygame
import sys
import random

# ---------------- Initialization ----------------
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Colors
BLACK = (10, 10, 10)
WHITE = (240, 240, 240)
GRAY = (100, 100, 100)

FONT = pygame.font.SysFont("consolas", 36)
BIG_FONT = pygame.font.SysFont("consolas", 56)

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

WINNING_SCORE = 5


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up:
            self.rect.y -= PADDLE_SPEED
        else:
            self.rect.y += PADDLE_SPEED
        self.rect.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)


def draw_middle_line():
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 15))


def draw_scores(left_score, right_score):
    left_surf = FONT.render(str(left_score), True, WHITE)
    right_surf = FONT.render(str(right_score), True, WHITE)
    screen.blit(left_surf, (WIDTH // 4, 20))
    screen.blit(right_surf, (WIDTH * 3 // 4, 20))


def show_message(text, y_offset=0, font=BIG_FONT, color=WHITE):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)


def main():
    left_paddle = Paddle(30)
    right_paddle = Paddle(WIDTH - 30 - PADDLE_WIDTH)
    ball = Ball()

    left_score = 0
    right_score = 0
    game_over = False
    winner_text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    left_score = 0
                    right_score = 0
                    ball.reset()
                    game_over = False
                elif game_over and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            # Left paddle: W/S
            if keys[pygame.K_w]:
                left_paddle.move(up=True)
            if keys[pygame.K_s]:
                left_paddle.move(up=False)

            # Right paddle: Up/Down arrows
            if keys[pygame.K_UP]:
                right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                right_paddle.move(up=False)

            ball.move()

            # Ball collision with paddles
            if ball.rect.colliderect(left_paddle.rect) and ball.speed_x < 0:
                ball.speed_x *= -1
            if ball.rect.colliderect(right_paddle.rect) and ball.speed_x > 0:
                ball.speed_x *= -1

            # Scoring
            if ball.rect.left <= 0:
                right_score += 1
                ball.reset()
            elif ball.rect.right >= WIDTH:
                left_score += 1
                ball.reset()

            if left_score >= WINNING_SCORE:
                game_over = True
                winner_text = "Left Player Wins!"
            elif right_score >= WINNING_SCORE:
                game_over = True
                winner_text = "Right Player Wins!"

        # ---------------- Drawing ----------------
        screen.fill(BLACK)
        draw_middle_line()
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()
        draw_scores(left_score, right_score)

        if game_over:
            show_message(winner_text, y_offset=-20)
            show_message("Press R to Restart or Q to Quit", y_offset=30, font=FONT)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
