import pygame
import random
import json
from js import document, window
from pyodide.ffi import create_proxy

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
GAME_SPEED = 10

# Initialize the canvas
canvas = document.getElementById('gameCanvas')
canvas.width = WINDOW_WIDTH
canvas.height = WINDOW_HEIGHT
screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            stored_score = window.localStorage.getItem('snake_high_score')
            return int(stored_score) if stored_score else 0
        except:
            return 0

    def save_high_score(self):
        window.localStorage.setItem('snake_high_score', str(self.high_score))

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[2:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color,
                           (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def handle_keys(event, snake):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and snake.direction != DOWN:
            snake.direction = UP
        elif event.key == pygame.K_DOWN and snake.direction != UP:
            snake.direction = DOWN
        elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
            snake.direction = LEFT
        elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
            snake.direction = RIGHT

def game_loop(time):
    global snake, food
    
    # Handle events
    for event in pygame.event.get():
        handle_keys(event, snake)

    # Update snake
    if not snake.update():
        if snake.score > snake.high_score:
            snake.high_score = snake.score
            snake.save_high_score()
        snake.reset()
        food.randomize_position()

    # Check if snake ate the food
    if snake.get_head_position() == food.position:
        snake.length += 1
        snake.score += 10
        food.randomize_position()

    # Draw everything
    screen.fill(BLACK)
    
    # Draw grid background
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, DARK_GREEN,
                               (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Render snake and food
    snake.render(screen)
    food.render(screen)

    # Draw scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {snake.score}', True, WHITE)
    high_score_text = font.render(f'High Score: {snake.high_score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    # Update canvas
    canvas_ctx = canvas.getContext('2d')
    canvas_ctx.drawImage(screen._canvas, 0, 0)
    
    # Request next frame
    window.requestAnimationFrame(create_proxy(game_loop))

# Initialize game objects
snake = Snake()
food = Food()

# Start the game loop
window.requestAnimationFrame(create_proxy(game_loop)) 