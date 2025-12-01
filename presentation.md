# Tetris Game Development
## Features & Design Patterns

**A Modern Implementation with Professional Architecture**

---

## Agenda

1. Project Overview
2. Feature Deep Dive (6 Major Features)
3. Gang of Four Design Patterns (7 Patterns)
4. Technical Architecture
5. Demo & Q&A

---

# Part 1: Project Overview

---

## What We Built

A **feature-rich Tetris implementation** that combines:

- ✅ Classic gameplay mechanics
- ✅ Modern software architecture
- ✅ Cloud persistence
- ✅ Player customization
- ✅ Professional code quality

**Tech Stack**: Python 3.12, Pygame 2.6.1, Supabase 2.20.0

---

## Development Philosophy

### Three Core Principles

1. **Clean Code** - Readable, maintainable, extensible
2. **User Experience** - Responsive, engaging, customizable
3. **Design Patterns** - Professional architecture using Gang of Four patterns

---

# Part 2: Feature Deep Dive

---

## Feature 1: Code Refactoring

### The Problem
- Original code had unclear variable names
- Magic numbers scattered throughout
- Duplicated logic
- Poor separation of concerns

### The Solution
✅ Descriptive naming conventions  
✅ Named constants for all values  
✅ Class-based architecture (`Piece`, `Board`, `Game`, `Menu`)  
✅ Separated UI from game logic  

---

## Code Refactoring: Example

### Before
```python
if p[0] < 0 or p[0] > 9 or p[1] > 19:
    return True
```

### After
```python
if (board_x < 0 or board_x >= self.width or 
    board_y >= self.height):
    return True
```

**Result**: Self-documenting code that's easy to understand and modify

---

## Feature 2: Sound Effects & Audio

### Audio Integration

Immersive audio feedback enhances player engagement

| Event | Sound File | Purpose |
|-------|-----------|---------|
| **Piece Lands** | `bloop-short.mp3` | Tactile feedback |
| **Line Clear** | `debris-break.mp3` | Satisfying reward |
| **Background** | `intro-theme.mp3` | Ambient atmosphere |

**Technical Details**:
- Pygame mixer module
- Background music loops at 0.3x volume
- Event-driven sound triggering
- Clean audio management (no overlap)

---

## Feature 3: Proper Block Movement

### Robust Collision Detection System

**Boundary Checking**
- Prevents movement beyond board edges
- Validates both horizontal and vertical constraints
- Checks collisions with placed blocks

**Movement Validation**
```python
def move(self, dx, dy, board):
    old_x, old_y = self.x, self.y
    self.x += dx
    self.y += dy
    
    if board.collides(self):
        self.x, self.y = old_x, old_y  # Revert
        return False
    return True
```

---

## Block Movement: Supported Pieces

All 7 standard Tetris pieces with accurate physics:

| Piece | Type | Rotations |
|-------|------|-----------|
| I-piece | Straight line | 2 |
| Z-piece | Zigzag | 2 |
| S-piece | Reverse zigzag | 2 |
| J-piece | L-shaped left | 4 |
| L-piece | L-shaped right | 4 |
| T-piece | T-shaped | 4 |
| O-piece | Square | 1 |

**Controls**: Left/Right navigation, soft drop, hard drop, rotation

---

## Feature 4: Next Block Preview

### Strategic Planning Feature

**Visual Design**
- Dedicated preview box on screen
- "Next Piece" label
- Theme-integrated styling
- Position: (350, 100) for visibility

**Benefits**
- 🧠 Enables strategic planning
- 📈 Improves skill development
- 🎯 Reduces surprise factor
- ⚡ Adds anticipation

---

## Next Block Preview: Implementation

```python
def spawn_new_piece(self):
    if self.next_piece is None:
        self.next_piece = Piece()  # Initialize first time
    
    self.current_piece = self.next_piece
    self.next_piece = Piece()  # Generate next
```

**User Experience**: Players can see what's coming and adapt their strategy accordingly

---

## Feature 5: Cloud Leaderboard

### Persistent Score Tracking with Supabase

**Architecture**
- Cloud-based database (Supabase PostgREST)
- Stores player names and scores
- Real-time synchronization
- Secure anonymous access

**Features**
- 🏆 Top 5 score display
- 💾 Permanent cloud storage
- 🔄 Automatic refresh after games
- 🎮 Name entry on game over

---

## Leaderboard: Technical Implementation

```python
# Score submission
def submit_score(name, score):
    supabase.table("Leaderboard").insert({
        "name": name, 
        "score": score
    }).execute()

# Fetch top scores
def get_leaderboard():
    response = supabase.table("Leaderboard")\
        .select("*")\
        .order("score", desc=True)\
        .limit(5)\
        .execute()
    return response.data
```

**Error Handling**: Graceful fallback if database unavailable

---

## Feature 6: Customizable Key Bindings

### Player Control Personalization

**Rebindable Actions**
- Move Left (default: ← Arrow)
- Move Right (default: → Arrow)  
- Move Down (default: ↓ Arrow)
- Rotate (default: ↑ Arrow)
- Hard Drop (default: Space)

**Access**: Settings → Controls menu

---

## Key Bindings: Rebinding Process

### User-Friendly Workflow

1. Select control to customize
2. Prompt: "Press a key..."
3. Next key pressed becomes new binding
4. ESC to cancel
5. "Reset to Defaults" option available

**Benefits**
- ♿ Accessibility for different equipment
- 🎮 Accommodates play styles
- 👈 Supports left-handed players
- 🔄 Easy to modify anytime

---

# Part 3: Gang of Four Design Patterns

---

## Why Design Patterns?

### Benefits of Gang of Four Patterns

- ✅ **Proven solutions** to common problems
- ✅ **Better communication** among developers
- ✅ **More maintainable** code
- ✅ **Easier to extend** and modify
- ✅ **Industry standard** practices

**We implemented 7 patterns in this project**

---

## Pattern 1: State Pattern

### Managing Application States

**Purpose**: Encapsulate state-specific behavior

**Implementation**:
```python
# Game states
game.state = "playing"       # Active gameplay
game.state = "gameover"      # Results screen
game.state = "entering_name" # Score submission

# Menu states  
menu.state = "main"          # Main menu
menu.state = "settings"      # Settings menu
menu.state = "controls"      # Control rebinding
```

**Benefits**: Clear state transitions, encapsulated behavior

---

## State Pattern: Impact

### Before Pattern
```python
if playing and not game_over and not entering_name:
    # gameplay logic
elif game_over and not entering_name:
    # game over logic
elif entering_name:
    # name input logic
```

### After Pattern
```python
if self.state == "playing":
    self.handle_gameplay()
elif self.state == "gameover":
    self.handle_game_over()
elif self.state == "entering_name":
    self.handle_name_input()
```

**Result**: Much cleaner and easier to extend!

---

## Pattern 2: Strategy Pattern

### Theme System as Strategy

**Purpose**: Encapsulate rendering strategies

**Implementation**:
```python
THEMES = {
    "Classic": {
        "background": (121, 121, 121),
        "board": (0, 0, 0),
        "outline": (0, 242, 242),
        "text": BLACK
    },
    "Starry": { ... },
    "Dark": { ... }
}

# Runtime strategy selection
self.theme = THEMES[theme_name]
```

---

## Strategy Pattern: Benefits

### Eliminates Conditional Logic

**Without Strategy**:
```python
if theme == "Classic":
    background = (121, 121, 121)
    outline = (0, 242, 242)
elif theme == "Starry":
    background = BLACK
    outline = (143, 128, 179)
# ... more conditions
```

**With Strategy**:
```python
pygame.draw.rect(screen, self.theme["background"], rect)
pygame.draw.rect(screen, self.theme["outline"], outline, 2)
```

**Benefits**: Runtime switching, data-driven design, easy to add themes

---

## Pattern 3: Factory Pattern

### Piece Creation

**Purpose**: Centralize object creation logic

**Implementation**:
```python
class Piece:
    def __init__(self, x=3, y=0):
        self.type = random.randint(0, len(PIECES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

class Game:
    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Piece()  # Factory creates
```

**Benefits**: Encapsulated randomization, simplified testing

---

## Factory Pattern: Testing Advantage

### Easy to Override for Tests

```python
# Production: Random pieces
piece = Piece()  

# Testing: Controlled pieces
piece = Piece(x=5, y=0)
piece.type = 0  # Force I-piece
piece.color = 1  # Force cyan
```

**Result**: Deterministic unit tests while maintaining random gameplay

---

## Pattern 4: Observer Pattern

### Event-Driven Audio System

**Purpose**: Decouple event sources from observers

**Implementation**:
```python
def freeze_current_piece(self):
    # Place piece on board
    self.board.place_piece(self.current_piece)
    
    # Notify observers
    self.sounds['placed'].play()  # Audio observer 1
    
    lines_cleared = self.board.clear_lines()
    if lines_cleared > 0:
        self.sounds['line_clear'].play()  # Audio observer 2
        self.score += lines_cleared ** 2
```

---

## Observer Pattern: Benefits

**Decoupled Architecture**
- Game logic doesn't know about audio system
- Easy to add new observers (particle effects, logging, etc.)
- Multiple observers respond to single event
- Clean separation of concerns

**Example**: When piece freezes:
1. 🔊 Sound plays
2. 🎨 Board updates
3. 📊 Score increases
4. 🎯 Next piece spawns

All without tight coupling!

---

## Pattern 5: Composite Pattern

### Board Grid Structure

**Purpose**: Treat individual and groups uniformly

**Implementation**:
```python
class Board:
    def __init__(self, width=10, height=20):
        # Composite structure: grid of cells
        self.grid = [[0 for _ in range(width)] 
                     for _ in range(height)]
    
    def place_piece(self, piece):
        # Operate on multiple cells as unit
        for i in range(4):
            for j in range(4):
                if i * 4 + j in blocks:
                    self.grid[y][x] = piece.color
```

---

## Composite Pattern: Menu Hierarchy

**Menu as Composite**:
```python
class Menu:
    # Menu options are composite structures
    self.main_menu_options = [
        "Start Game", 
        "Settings", 
        "Quit"
    ]
    
    self.settings_menu_options = [
        "Theme", 
        "Controls", 
        "Back"
    ]
```

**Benefits**: Hierarchical structure, uniform operations, recursive composition

---

## Pattern 6: Template Method Pattern

### Consistent Input Handling

**Purpose**: Define operation skeleton, let subclasses implement steps

**Implementation**:
```python
# Template method
def handle_input(self, event):
    if event.type == pygame.KEYDOWN:
        if self.state == "main":
            return self._handle_main_menu_input(event)
        elif self.state == "settings":
            return self._handle_settings_menu_input(event)
        elif self.state == "controls":
            return self._handle_controls_menu_input(event)
```

---

## Template Method: Concrete Implementation

```python
# Concrete implementation for main menu
def _handle_main_menu_input(self, event):
    if event.key == pygame.K_UP:
        self.selected_option = (self.selected_option - 1) % len(...)
    elif event.key == pygame.K_DOWN:
        self.selected_option = (self.selected_option + 1) % len(...)
    elif event.key == pygame.K_RETURN:
        # Execute selected option
```

**Benefits**: Reduces duplication, ensures consistency, easy to extend

---

## Pattern 7: Singleton Pattern

### Single Resource Instance

**Purpose**: Guarantee single instance of critical resources

**Implementation**:
```python
# Singleton database client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Used throughout application
response = supabase.table("Leaderboard").select(...).execute()

# Single board per game
class Game:
    def __init__(self):
        self.board = Board(10, 20)  # One board instance
```

**Benefits**: Prevents duplicate connections, centralized access, thread-safe

---

## Design Patterns Summary

| Pattern | Purpose | Location |
|---------|---------|----------|
| **State** | Manage game/menu states | Game, Menu classes |
| **Strategy** | Theme rendering | THEMES dictionary |
| **Factory** | Piece creation | Piece.__init__ |
| **Observer** | Event-driven audio | Sound system |
| **Composite** | Board/menu structure | Grid, menus |
| **Template Method** | Input handling | Menu methods |
| **Singleton** | Resource management | Supabase, Board |

---

# Part 4: Technical Architecture

---

## System Architecture

### Class Hierarchy

```
Tetris Application
├── Piece
│   ├── Position (x, y)
│   ├── Type & Color
│   ├── Rotation state
│   └── Methods: move(), rotate(), drop()
├── Board
│   ├── Grid (10×20)
│   ├── Collision detection
│   └── Line clearing
├── Game
│   ├── Board instance
│   ├── Current & next piece
│   ├── Score & state
│   └── Game loop logic
└── Menu
    ├── Menu states
    ├── Theme management
    └── Key binding config
```

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Frame Rate** | 25 FPS |
| **Window Size** | 600 × 500 pixels |
| **Board Dimensions** | 10 × 20 cells |
| **Block Size** | 20 × 20 pixels |
| **Drop Speed** | 2 cells per frame cycle |

**Optimization**: Efficient collision detection, minimal redraws

---

## Project Structure

```
TetrisMergeConflicts/
├── Tetris.py              # Main application (800+ lines)
├── test_tetris.py         # Comprehensive unit tests
├── assets/                # Audio resources
│   ├── intro-theme.mp3
│   ├── bloop-short.mp3
│   └── debris-break.mp3
├── pyproject.toml         # Dependencies (uv)
├── README.md              # Quick start guide
└── docs/                  # Hugo documentation site
    ├── config.toml
    └── content/
```

---

## Testing Strategy

### Comprehensive Unit Tests

**Coverage**:
- ✅ Piece movement and rotation
- ✅ Collision detection
- ✅ Line clearing algorithm
- ✅ Board state management
- ✅ Mock Supabase integration

**Run Tests**:
```bash
python -m unittest test_tetris.py
```

**Result**: High confidence in core game mechanics

---

## Dependencies

### Production Dependencies

```toml
[project]
dependencies = [
    "pygame>=2.6.1",
    "supabase>=2.20.0"
]
requires-python = ">=3.12"
```

**Why these choices?**
- **Pygame**: Industry-standard game library
- **Supabase**: Modern, scalable backend
- **Python 3.12**: Latest stable features

---

## Database Schema

### Supabase Leaderboard Table

```sql
CREATE TABLE Leaderboard (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_score ON Leaderboard(score DESC);
```

**Features**:
- Auto-incrementing ID
- Timestamp tracking
- Indexed for fast queries

---

## Theme System Architecture

### Three Built-in Themes

**Classic Theme**
- Gray background (121, 121, 121)
- Cyan outline (0, 242, 242)
- Traditional Tetris aesthetic

**Starry Theme**
- Dark background with purple board
- Violet highlights (143, 128, 179)
- Mystical appearance

**Dark Theme** (Default)
- Minimalist dark gray (20, 20, 20)
- White text for contrast
- Modern, professional look

---

## Key Binding System

### Flexible Control Scheme

**Default Bindings**:
```python
DEFAULT_KEYBINDS = {
    "move_left": pygame.K_LEFT,
    "move_right": pygame.K_RIGHT,
    "move_down": pygame.K_DOWN,
    "rotate": pygame.K_UP,
    "hard_drop": pygame.K_SPACE
}
```

**Features**:
- Runtime rebinding
- Session persistence
- Reset to defaults
- Validation against conflicts

---

# Key Achievements

---

## What We Accomplished

### Code Quality
✅ **Clean Architecture** - Well-organized, maintainable code  
✅ **Design Patterns** - 7 Gang of Four patterns applied  
✅ **Comprehensive Tests** - Unit tests for critical components  
✅ **Documentation** - Hugo site with full docs  

### User Experience
✅ **Immersive Audio** - Background music + sound effects  
✅ **Visual Themes** - 3 customizable themes  
✅ **Flexible Controls** - Rebindable key bindings  
✅ **Strategic Gameplay** - Next block preview  

### Modern Features
✅ **Cloud Persistence** - Supabase leaderboard  
✅ **Professional UI** - Polished menu system  
✅ **Error Handling** - Graceful failure recovery  

---

## Lessons Learned

### Technical Insights

1. **Design patterns aren't overhead** - They simplify complex systems
2. **Refactoring pays dividends** - Clean code is faster to modify
3. **User feedback matters** - Audio/visual cues enhance engagement
4. **Testing saves time** - Caught bugs before they reached users

### Team Collaboration

- Clear code = easier collaboration
- Consistent patterns = shared understanding
- Documentation = knowledge transfer

---

## Future Enhancements

### Potential Features

**Gameplay**
- 🎚️ Difficulty levels with speed scaling
- 🤝 Multiplayer competitive mode
- ⚡ Power-ups and special pieces
- 🎯 Combo system with bonus points

**Technical**
- 🔊 Volume controls in settings
- 💾 Local high score backup
- 🏆 Achievement/medal system
- ✨ Particle effects for line clears

**Platform**
- 📱 Mobile port
- 🌐 Web version (Pygame Web)
- 🎮 Gamepad support

---

## Live Demo

### Running the Game

```bash
# Clone repository
git clone https://github.com/Pbierley/TetrisMergeConflicts.git
cd TetrisMergeConflicts

# Run with uv (recommended)
uv run Tetris.py

# Or with Python
pip install pygame supabase
python Tetris.py
```

**Let's see it in action!** 🎮

---

## Resources

### Links

- 🌐 **Documentation Site**: https://pbierley.github.io/TetrisMergeConflicts/
- 💻 **GitHub Repository**: https://github.com/Pbierley/TetrisMergeConflicts
- 📚 **Gang of Four Patterns**: Design Patterns book (Gamma et al.)

### Contact

- Questions?
- Suggestions?
- Want to contribute?

**Open an issue or pull request!**

---

# Questions?

## Thank you for your attention!

**Key Takeaways**:
1. Design patterns make code better
2. User experience drives engagement
3. Clean architecture enables growth
4. Testing prevents regression

---

# End of Presentation

**Thank you!**
