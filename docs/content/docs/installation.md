---
title: "Installation & Setup"
weight: 3
---

# Installation Guide

## System Requirements

- Python 3.12 or higher
- Pygame 2.6.1 or higher
- Supabase 2.20.0 or higher

---

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/Pbierley/TetrisMergeConflicts
cd TetrisMergeConflicts
```

### 2. Install Dependencies

**Using `uv` (recommended):**

```bash
uv pip install -r requirements.txt
```

**Or with pip:**

```bash
pip install pygame>=2.6.1 supabase>=2.20.0
```

### 3. Run Game

```bash
uv run Tetris.py
```

Or:

```bash
python Tetris.py
```

---

## Running Tests

```bash
python -m unittest test_tetris.py
```

---

## Configuration

Game settings in `Tetris.py`:

```python
WINDOW_SIZE = (600, 500)     # Window dimensions
COLORS = (...)               # Color palette
PIECES = [...]               # Tetromino shapes
THEMES = {...}               # Visual themes
DEFAULT_KEYBINDS = {...}     # Control mappings
```

---

## Troubleshooting

### "ModuleNotFoundError: pygame"

Install pygame:

```bash
pip install pygame
```

### "No audio files found"

Ensure `assets/` folder contains:
- `intro-theme.mp3`
- `bloop-short.mp3`
- `debris-break.mp3`

### Game runs but no sound

Check volume settings in OS and verify audio files exist in `assets/`
