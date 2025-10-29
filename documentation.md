---
marp: true
size: 4:3
paginate: true
---

# Tetris Game Documentation

This file implements a classic Tetris game using the **Pygame** library for graphics and game loop management. It also integrates with **Supabase** for score persistence, saving the final game score to a `Leaderboard` table.

---

## 1) Dependencies and Setup

The script requires `pygame` for the game and `supabase` for the database integration.

| Library  | Purpose                                                                 |
|----------|-------------------------------------------------------------------------|
| `pygame` | Handles graphics, audio, input, and the main game loop.                 |
| `supabase` | Connects to and interacts with a Supabase database (score saving).   |

---

### Supabase Configuration

| Constant        | Value                                           | Purpose                                      |
|-----------------|--------------------------------------------------|----------------------------------------------|
| `SUPABASE_URL`  | `"https://ddafhennccnnqlzdaxer.supabase.co"`    | Base URL for the Supabase project.           |
| `SUPABASE_KEY`  | `"[...snipped for brevity...]"`                 | Anon Public Key used for client access.      |
| `supabase`      | *Client object*                                  | Configured Supabase client instance.         |

---

## 2) Core Constants and Data Structures

| Constant                     | Description |
|-----------------------------|-------------|
| `COLORS`                    | Tuple of RGB color tuples. Index `0` is Black (empty cell); indices `1–7` map to Tetris piece colors. |
| `BLACK`, `WHITE`, `GRAY`    | Standard RGB color definitions used for drawing. |
| `PIECES`                    | List of the 7 classic Tetris pieces (I, Z, S, J, L, T, O). Each piece is a list of rotation states; a rotation state is a list of occupied cell indices in a 4×4 grid. |
| `WINDOW_SIZE`               | Tuple `(600, 500)` defining the Pygame window dimensions. |

---

## 3) Class Definitions

### 3.1 Piece 🧱
Represents a single falling Tetris piece.

| Method | Description |
|-------|-------------|
| `__init__(self, x=3, y=0)` | Initializes the piece at a starting position, with a random type (`0–6`), random color (`1–7`), and rotation `0`. |
| `get_blocks(self)` | Returns the block indices for the piece’s current type and rotation. |
| `move(self, dx, dy, board)` | Attempts to move by `(dx, dy)`. Uses `board.collides()` to detect collisions. Returns `True` if moved, `False` otherwise. |
| `rotate(self, board)` | Attempts to rotate to the next state; reverts if a collision occurs. |
| `drop_to_bottom(self, board)` | Moves the piece down until a collision would occur. |

---

### 3.2 Board 🗺️
Represents the fixed playing field; handles placement and line clearing.

**Attributes**

| Attribute        | Description |
|------------------|-------------|
| `width`, `height`| Grid dimensions (default `10×20`). |
| `grid`           | 2D list representing board state; cells contain color index (`0` for empty). |

**Methods**

| Method | Description |
|-------|-------------|
| `collides(self, piece)` | Checks if `piece` overlaps boundaries or placed blocks. |
| `place_piece(self, piece)` | Freezes the piece by writing its color indices to `self.grid`. |
| `clear_lines(self)` | Removes any full rows (via `_is_line_full()` and `_remove_line()`); returns count of lines cleared. |
| `_is_line_full(self, row)` | Helper: returns `True` if all cells in a row are occupied (`> 0`). |
| `_remove_line(self, row_to_remove)` | Helper: removes the given row and inserts an empty row at the top. |

---

### 3.3 Game 🎮
Manages overall game state, score, pieces, and logic.

**Attributes**

| Attribute        | Description |
|------------------|-------------|
| `board`          | Instance of `Board`. |
| `current_piece`  | The currently falling piece. |
| `next_piece`     | The next piece (for preview). |
| `score`          | Current player score.

---