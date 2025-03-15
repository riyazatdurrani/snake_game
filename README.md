# Snake Game

A classic Snake game implementation with a modern UI and high score tracking.

## Features
- Smooth snake movement
- High score tracking (persisted between game sessions)
- Modern UI with grid background
- Score display
- Collision detection
- Wrap-around boundaries

## Requirements
- Python 3.x
- Pygame

## Installation
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play
1. Run the game:
```bash
python snake_game.py
```

2. Controls:
- Use arrow keys to control the snake's direction
- Try to eat the red food to grow and increase your score
- Avoid colliding with yourself
- The game saves your high score automatically

## Game Rules
- Each food eaten increases your score by 10 points
- The snake wraps around the screen edges
- Game over occurs when the snake collides with itself
- Your high score is automatically saved and loaded between sessions 