import pygame
from pygame.locals import *
import time
import random
import os

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
RESOURCE_DIR = "resources"


def resource_path(filename):
    return os.path.join(RESOURCE_DIR, filename)


def safe_load_image(filename, fallback_color, size=(SIZE, SIZE)):
    """Load an image if it exists, otherwise return a plain colored surface."""
    path = resource_path(filename)
    if os.path.isfile(path):
        try:
            return pygame.image.load(path).convert()
        except pygame.error:
            pass
    surface = pygame.Surface(size)
    surface.fill(fallback_color)
    return surface


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = safe_load_image("apple.jpg", (220, 30, 30))
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = safe_load_image("block.jpg", (0, 200, 0))
        self.direction = "down"

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def walk(self):
        # update body: each segment moves to where the one in front of it was
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")

        self.surface = pygame.display.set_mode((1000, 800))
        self.background = safe_load_image(
            "background.jpg", BACKGROUND_COLOR, size=(1000, 800)
        )

        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        self.surface.blit(self.background, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collision(
            self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y
        ):
            self.snake.increase_length()
            self.apple.move()

        # wall collision
        if not (0 <= self.snake.x[0] < 1000) or not (0 <= self.snake.y[0] < 800):
            raise Exception("Hit the wall")

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(
                self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                raise Exception("Collision Occurred")

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(
            f"Score: {self.snake.length}", True, (200, 200, 200)
        )
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(
            f"Game is over! Your score is {self.snake.length}",
            True,
            (255, 255, 255),
        )
        self.surface.blit(line1, (200, 300))
        line2 = font.render(
            "To play again press Enter. To exit press Escape!",
            True,
            (255, 255, 255),
        )
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.25)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
