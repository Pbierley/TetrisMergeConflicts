---
title: "Architecture & Design Patterns"
weight: 2
---

# Software Architecture

## Design Patterns (Gang of Four)

### 1. State Pattern
Manages different application states (playing, menu, game over, entering_name).
```python
game.state = "playing"      # Active gameplay
game.state = "gameover"     # Game over screen
game.state = "entering_name" # Name input
```

Benefits: Encapsulated state-specific behavior, clear state transitions

### 2. Strategy Pattern
Theme system encapsulates rendering strategies.
```python
THEMES = {
    "Classic": { "background": (121, 121, 121), ... },
    "Starry": { "background": BLACK, ... },
    "Dark": { "background": (20, 20, 20), ... }
}
self.theme = THEMES[theme_name]
```

Benefits: Runtime strategy switching, eliminates conditional logic

### 3. Factory Pattern
Centralized piece creation logic.
```python
class Game:
    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Piece()  # Factory creates piece
```

Benefits: Encapsulates randomization, simplifies testing

### 4. Observer Pattern
Event-driven audio system.
```python
def freeze_current_piece(self):
    self.sounds['placed'].play()      # Audio observer notified
    if lines_cleared > 0:
        self.sounds['line_clear'].play()  # Another observer
```

Benefits: Decoupled game logic from audio, easy to add new observers

### 5. Composite Pattern
Board grid and menu hierarchies.
```python
class Board:
    self.grid = [[0 for _ in range(width)] for _ in range(height)]

def place_piece(self, piece):  # Operates on composite structure
    for i in range(4):
        for j in range(4):
            if i * 4 + j in blocks:
                self.grid[board_y][board_x] = piece.color
```

Benefits: Uniform treatment of individual and group objects

### 6. Template Method Pattern
Consistent input handling across menu states.
```python
def handle_input(self, event):
    if self.state == "main":
        return self._handle_main_menu_input(event)
    elif self.state == "settings":
        return self._handle_settings_menu_input(event)
```

Benefits: Reduces duplication, ensures consistency

### 7. Singleton Pattern
Single database and board instance.
```python
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
self.board = Board(10, 20)  # One per game
```

Benefits: Guarantees single instance, prevents duplicate connections

## Class Hierarchy
Piece
├── x, y (position)
├── type (0-6 for 7 piece types)
├── color (1-7 for colors)
├── rotation (0-3 for rotations)
├── get_blocks()
├── move(dx, dy, board)
├── rotate(board)
└── drop_to_bottom(board)
Board
├── width, height (10x20)
├── grid (2D array)
├── collides(piece)
├── place_piece(piece)
├── clear_lines()
└── _is_line_full(row)
Game
├── board
├── current_piece
├── next_piece
├── score
├── state
├── spawn_new_piece()
├── move_piece(dx, dy)
├── rotate_piece()
├── drop_piece()
├── tick()
└── freeze_current_piece()
Menu
├── state (main, settings, controls)
├── selected_option
├── theme
├── keybinds
├── handle_input(event)
└── draw(screen)

## Performance

| Metric | Value |
|--------|-------|
| FPS | 25 frames per second |
| Window Size | 600 × 500 pixels |
| Board Dimensions | 10 × 20 cells |
| Block Size | 20 × 20 pixels |
| Piece Drop Speed | 2 moves per FPS cycle |

## Dependencies

- **Pygame 2.6.1+** - Graphics, audio, input
- **Supabase 2.20.0+** - Cloud database
- **Python 3.12+** - Runtime