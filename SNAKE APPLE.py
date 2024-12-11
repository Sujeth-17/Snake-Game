import pygame
import time
import random

# Constants
SIZE = 40
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Apple Class
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png").convert_alpha()
        self.x = random.randint(0, SCREEN_WIDTH // SIZE - 1) * SIZE
        self.y = random.randint(0, SCREEN_HEIGHT // SIZE - 1) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, SCREEN_WIDTH // SIZE - 1) * SIZE
        self.y = random.randint(0, SCREEN_HEIGHT // SIZE - 1) * SIZE


# Snake Class
class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("square.png").convert_alpha()
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "right"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

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
        self.parent_screen.fill((0, 0, 0))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


# Game Class
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.snake = Snake(self.screen, 1)
        self.apple = Apple(self.screen)
        self.game_over_flag = False

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True
        return False

    def display_score(self):
        font = pygame.font.SysFont("comicsans", 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.screen.blit(score, (850, 10))

    def play(self):
        if not self.game_over_flag:
            self.snake.walk()
            self.apple.draw()
            self.display_score()

            # Check for collision with apple
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                self.snake.increase_length()
                self.apple.move()

            # Check for collision with self
            for i in range(1, self.snake.length):
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    self.game_over_flag = True

            # Check for collision with wall
            if (
                self.snake.x[0] < 0
                or self.snake.x[0] >= SCREEN_WIDTH
                or self.snake.y[0] < 0
                or self.snake.y[0] >= SCREEN_HEIGHT
            ):
                self.game_over_flag = True

        pygame.display.flip()

    def show_game_over(self):
        self.screen.fill((255, 0, 0))
        font = pygame.font.SysFont("comicsans", 50)
        message = font.render(f"Game Over! Your score: {self.snake.length - 1}", True, (255, 255, 255))
        self.screen.blit(message, (200, 300))
        pygame.display.flip()
        time.sleep(3)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if not self.game_over_flag:
                        if event.key == pygame.K_UP:
                            self.snake.move_up()
                        if event.key == pygame.K_DOWN:
                            self.snake.move_down()
                        if event.key == pygame.K_LEFT:
                            self.snake.move_left()
                        if event.key == pygame.K_RIGHT:
                            self.snake.move_right()

            if self.game_over_flag:
                self.show_game_over()
                running = False
            else:
                self.play()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
