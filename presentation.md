# Tetris Game Development: Features Overview

## Project Summary

This document outlines the key features and improvements implemented during the development of our Tetris game. The project focused on creating a modern, maintainable codebase with enhanced gameplay mechanics and user experience features.

---

## 1. Code Refactoring & Architecture Improvement

### Overview
The codebase underwent significant refactoring to improve clarity, maintainability, and extensibility for future development.

### Key Improvements

**Variable & Function Naming**
- Replaced unclear variable names with descriptive identifiers
- Improved code readability by following consistent naming conventions
- Made the codebase more self-documenting and easier to understand

**Magic Numbers Removal**
- Extracted hardcoded values into named constants
- Created dedicated configuration sections for easy adjustment of game parameters
- Enhanced code maintainability by centralizing value definitions

**Code Organization**
- Separated concerns into distinct classes: `Piece`, `Board`, `Game`, and `Menu`
- Removed duplicated logic and consolidated common operations
- Implemented proper encapsulation for game state management
- Created reusable functions for drawing and game operations

**Design Patterns**
- Applied object-oriented principles for cleaner architecture
- Implemented state management patterns for game flow control
- Separated UI rendering logic from game logic

---

## 2. Sound Effects & Audio Integration

### Overview
Added immersive audio feedback to enhance player engagement and game feel.

### Features Implemented

**Sound Library Integration**
- Integrated Pygame's mixer module for audio playback
- Loaded and managed multiple sound effect files efficiently

**Game Audio Events**

| Event | Sound | Purpose |
|-------|-------|---------|
| **Piece Placement** | Bloop sound (`bloop-short.mp3`) | Auditory feedback when blocks land |
| **Line Clear** | Debris break sound (`debris-break.mp3`) | Satisfying feedback for completing lines |
| **Background Music** | Intro theme (`intro-theme.mp3`) | Looping background ambiance during gameplay |

**Audio Features**
- Background music loops continuously at reduced volume (0.3x)
- Sound effects trigger on appropriate game events
- Audio assets load from a dedicated `assets/` directory
- Clean audio management prevents overlap and cacophony

---

## 3. Proper Block Movement Mechanics

### Overview
Implemented robust collision detection and movement validation to ensure precise gameplay mechanics.

### Collision Detection System

**Boundary Checking**
- Prevents pieces from moving beyond board edges
- Validates both horizontal and vertical boundary constraints
- Checks for collisions with previously placed blocks

**Movement Validation**
- `move()` method attempts movement then validates against collisions
- Reverts position if collision detected
- Returns success/failure status for UI feedback

**Piece Types Supported**
- I-piece (straight line)
- Z-piece and S-piece (zigzag patterns)
- J-piece and L-piece (corner pieces)
- T-piece (T-shaped)
- O-piece (square)

### Movement Controls
- Left/Right navigation with boundary checking
- Downward movement with collision detection
- Soft drop functionality for controlled descent
- Hard drop for instant placement

---

## 4. Next Block Preview Feature

### Overview
Displays the upcoming Tetromino before it enters the playing field, allowing players to plan ahead.

### Implementation Details

**Visual Design**
- Dedicated preview box positioned on the game screen
- Clear label: "Next Piece"
- Styled border and background for visual distinction
- Integrated with current theme system

**Functionality**
- Previews the next piece before it spawns
- Updates automatically after each piece placement
- Uses same rendering system as falling pieces
- Positioned at coordinates (350, 100) for optimal visibility

**User Experience Benefits**
- Enables strategic planning
- Reduces surprise and improves skill development
- Adds anticipation and engagement
- Helps players adapt to upcoming piece types

---

## 5. Persistent Leaderboard System

### Overview
Implemented a cloud-based leaderboard that persists scores between game sessions using Supabase.

### Architecture

**Database Integration**
- Connected to Supabase backend for secure data storage
- Stores player names and scores in a `Leaderboard` table
- Uses anonymous public key for client-side access

**Features**

| Feature | Details |
|---------|---------|
| **Score Submission** | Players enter names after game over |
| **Top 5 Display** | Leaderboard shows highest scores in real-time |
| **Persistent Storage** | Scores saved indefinitely in cloud |
| **Automatic Refresh** | Leaderboard updates after each new score |

**User Flow**
1. Game ends and player enters their name
2. Score automatically submitted to database
3. Leaderboard fetched and displayed on game screen
4. Player can view rankings before next game

**Technical Implementation**
- Uses Supabase PostgREST API for database operations
- Implements error handling for network failures
- Graceful fallback if database unavailable
- Efficient sorting and limiting queries (top 5)

---

## 6. Customizable Key Binding System

### Overview
Allows players to customize game controls according to personal preferences.

### Key Binding Features

**Supported Actions**
- Move Left (default: LEFT ARROW)
- Move Right (default: RIGHT ARROW)
- Move Down (default: DOWN ARROW)
- Rotate (default: UP ARROW)
- Hard Drop (default: SPACEBAR)

**Customization System**

**Settings Menu Integration**
- Access controls from main settings menu
- Visual display of current key bindings
- Real-time rebinding interface

**Rebinding Process**
1. Select control to customize
2. Prompt displays "Press a key..."
3. Next key pressed becomes new binding
4. Press ESC to cancel rebinding
5. "Reset to Defaults" option available

**Persistence**
- Keybinds maintained during current session
- Passed between menu and game states
- Preserved when returning to menu

**Benefits**
- Accommodates different play styles
- Improves accessibility for users with different equipment
- Supports left-handed players
- Reduces learning curve for experienced Tetris players

---

## 7. Theme System

### Overview
Provides visual variety and player personalization options.

### Available Themes

**Classic Theme**
- Gray background with cyan outline
- Traditional Tetris aesthetic
- Black text for contrast

**Starry Theme**
- Dark purple board with mystical appearance
- Violet highlights and outline
- Atmospheric gaming experience

**Dark Theme** (Default)
- Minimalist dark gray background
- Clean black board
- White text for maximum contrast
- Modern, professional appearance

### Theme Integration
- Selectable from settings menu
- Real-time theme switching during gameplay
- Affects: background, board, preview box, outline, and text colors
- Quick toggle keys (1, 2, 3) during gameplay

---

## 8. Menu System & Game States

### Overview
Comprehensive menu interface for navigation and settings management.

### Main Menu
- Start Game
- Settings
- Quit Application

### Settings Menu
- Theme Selection
- Control Rebinding
- Back to Main Menu

### Controls Menu
- Display current key bindings
- Rebind individual controls
- Reset to defaults
- Navigation with UP/DOWN arrows and ENTER to select

### Game States
- **Menu State**: Navigation and settings
- **Playing State**: Active gameplay
- **Entering Name State**: Score submission prompt
- **Game Over State**: Results display with replay/quit options

---

## Design Patterns (Gang of Four)

### 1. State Pattern

**Implementation**: Used throughout the `Game` and `Menu` classes to manage different application states.

**Usage**
```python
# Game states
game.state = "playing"      # Active gameplay
game.state = "gameover"     # Game over screen
game.state = "entering_name" # Name input prompt

# Menu states
menu.state = "main"         # Main menu
menu.state = "settings"     # Settings menu
menu.state = "controls"     # Control rebinding
```

**Benefits**
- Encapsulates state-specific behavior
- Simplifies conditional logic
- Makes state transitions explicit and clear
- Enables easy addition of new states

**Example**: When `game.state == "entering_name"`, different input handling and rendering occurs than when `game.state == "playing"`.

---

### 2. Strategy Pattern

**Implementation**: Used with the theme system to encapsulate rendering strategies.

**Usage**
```python
THEMES = {
    "Classic": { "background": (121, 121, 121), ... },
    "Starry":  { "background": BLACK, ... },
    "Dark":    { "background": (20, 20, 20), ... }
}

# Strategy selection at runtime
self.theme = THEMES[theme_name]
```

**Benefits**
- Encapsulates different rendering strategies (themes)
- Allows runtime strategy switching without code changes
- Eliminates conditional logic for theme selection
- Easy to add new themes

**Example**: Instead of `if theme == "Classic": ... elif theme == "Starry": ...`, we store strategy as data structure and apply it uniformly.

---

### 3. Factory Pattern

**Implementation**: Used in piece spawning and creation.

**Usage**
```python
class Piece:
    def __init__(self, x=3, y=0):
        self.type = random.randint(0, len(PIECES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

class Game:
    def spawn_new_piece(self):
        if self.next_piece is None:
            self.next_piece = Piece()  # Factory creates piece
        self.current_piece = self.next_piece
        self.next_piece = Piece()
```

**Benefits**
- Centralizes piece creation logic
- Encapsulates randomization and initialization
- Easy to modify piece creation without affecting game logic
- Simplifies testing with mock pieces

**Example**: Test cases use `Piece(x=5, y=0, piece_type=0, color_idx=1)` with specific parameters instead of random values.

---

### 4. Observer Pattern (Implicit)

**Implementation**: Used with the audio system and event-driven architecture.

**Usage**
```python
# Game "observes" piece placement events
if not self.current_piece.move(0, 1, self.board):
    self.freeze_current_piece()  # Triggers event

# Event handler responds to piece freeze
def freeze_current_piece(self):
    self.sounds['placed'].play()  # Observer notifies audio system
    lines_cleared = self.board.clear_lines()
    if lines_cleared > 0:
        self.sounds['line_clear'].play()  # Another observer notification
```

**Benefits**
- Decouples game logic from audio system
- Multiple observers can respond to single event
- Easy to add new observers (e.g., particle effects, logging)
- Clean separation of concerns

**Example**: When a piece freezes, multiple systems are notified: sound plays, board updates, score increases.

---

### 5. Composite Pattern

**Implementation**: Used in the board grid structure and menu hierarchies.

**Usage**
```python
# Board as composite of cells
class Board:
    def __init__(self, width=10, height=20):
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Composite operations
    def place_piece(self, piece):  # Places multiple blocks at once
        for i in range(4):
            for j in range(4):
                if i * 4 + j in blocks:
                    self.grid[board_y][board_x] = piece.color

# Menu hierarchy
class Menu:
    self.main_menu_options = ["Start Game", "Settings", "Quit"]
    self.settings_menu_options = ["Theme", "Controls", "Back"]
```

**Benefits**
- Treats individual cells and groups uniformly
- Hierarchical menu structure naturally represented
- Recursive composition for complex structures
- Simplifies operations on groups of objects

**Example**: `board.clear_lines()` operates on entire rows as composite units rather than individual cells.

---

### 6. Template Method Pattern

**Implementation**: Used in event handling throughout menu and game systems.

**Usage**
```python
# Template in Menu class
def handle_input(self, event):
    if event.type == pygame.KEYDOWN:
        if self.state == "main":
            return self._handle_main_menu_input(event)
        elif self.state == "settings":
            return self._handle_settings_menu_input(event)
        elif self.state == "controls":
            return self._handle_controls_menu_input(event)

# Each substate has specific implementation
def _handle_main_menu_input(self, event):  # Template method concrete implementation
    if event.key == pygame.K_UP:
        self.selected_option = (self.selected_option - 1) % len(...)
    elif event.key == pygame.K_DOWN:
        self.selected_option = (self.selected_option + 1) % len(...)
    elif event.key == pygame.K_RETURN:
        # State-specific actions
```

**Benefits**
- Defines skeleton of operation in base method
- Subclasses implement specific steps
- Reduces code duplication across similar operations
- Ensures consistent structure across states

**Example**: All menu input handling follows same pattern: arrow navigation, Enter selection, Escape cancellation.

---

### 7. Singleton Pattern (Implicit)

**Implementation**: Used with the Supabase client and game board.

**Usage**
```python
# Global supabase instance (singleton)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Used throughout application
response = supabase.table("Leaderboard").select(...).execute()

# Single board instance per game
class Game:
    def __init__(self):
        self.board = Board(10, 20)  # One board per game session
```

**Benefits**
- Guarantees single instance of critical resources
- Prevents multiple database connections
- Centralized access point
- Thread-safe resource management

**Example**: All leaderboard operations use same Supabase client instance.

---

## Technical Specifications

### Dependencies
- **Pygame 2.6.1+**: Graphics, audio, and input handling
- **Supabase 2.20.0+**: Cloud database for leaderboard persistence
- **Python 3.12+**: Language runtime

### Project Structure
```
Tetris/
├── Tetris.py              # Main game file
├── test_tetris.py         # Unit tests
├── assets/                # Audio files
│   ├── intro-theme.mp3
│   ├── bloop-short.mp3
│   └── debris-break.mp3
├── pyproject.toml         # Project configuration
└── README.md              # Quick start guide
```

### Testing
- Comprehensive unit tests for Piece and Board classes
- Collision detection validation
- Leaderboard functionality testing
- Mock Supabase integration for safe testing

### Design Pattern Summary

| Pattern | Purpose | Location |
|---------|---------|----------|
| **State** | Manage game/menu states | Game, Menu classes |
| **Strategy** | Theme rendering strategies | THEMES dictionary |
| **Factory** | Piece creation | Piece.__init__, Game.spawn_new_piece |
| **Observer** | Event-driven audio system | Sound effects triggering |
| **Composite** | Board structure & menu hierarchy | Board.grid, Menu options |
| **Template Method** | Consistent input handling | Menu.handle_input methods |
| **Singleton** | Single database/board instance | Supabase client, Board instance |

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **FPS** | 25 frames per second |
| **Window Size** | 600 × 500 pixels |
| **Board Dimensions** | 10 × 20 cells |
| **Block Size** | 20 × 20 pixels |
| **Piece Drop Speed** | 2 moves per FPS cycle |

---

## Future Enhancement Opportunities

- Difficulty levels with increasing speed
- Multiplayer competitive mode
- Sound volume controls in settings
- Local high score backup
- Power-ups and special pieces
- Combo system with bonus points
- Achievement/medal system
- Particle effects for line clears

---

## Conclusion

The Tetris game now features a polished, user-friendly experience with modern architecture and engaging gameplay mechanics. The combination of intuitive controls, visual feedback, and persistent online leaderboards creates a complete gaming experience that encourages player engagement and replayability.

### Key Achievements
✅ Clean, maintainable codebase  
✅ Immersive audio experience  
✅ Precise game mechanics  
✅ Strategic gameplay elements  
✅ Cloud-based persistence  
✅ Player customization options  
✅ Professional visual design  
✅ Robust error handling