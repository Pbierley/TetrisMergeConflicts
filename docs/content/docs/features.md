---
title: "Features"
weight: 1
---

# Game Features

## Core Gameplay

### Precise Block Movement
- Real-time collision detection
- Boundary validation
- Smooth piece control
- Hard drop support

### Next Block Preview
Plan ahead with a visible preview of the upcoming Tetromino before it spawns.

### Line Clearing System
Automatically detects and clears completed rows with score multiplier (lines²).

## Audio System

Complete audio integration using Pygame mixer:

| Event | Sound File | Effect |
|-------|-----------|--------|
| Piece Placement | `bloop-short.mp3` | Confirms block landing |
| Line Clear | `debris-break.mp3` | Satisfying completion feedback |
| Background | `intro-theme.mp3` | Looping atmospheric music at 0.3x volume |

## Cloud Leaderboard

### Supabase Integration
- Cloud-based score persistence
- Real-time top 5 rankings
- Player name submissions
- Automatic database synchronization

### Leaderboard Features
- Display active during gameplay
- Updates after each game
- Name input on game over
- Graceful error handling

## Customizable Controls

Five rebindable actions with visual feedback:

Move Left     → LEFT ARROW (rebindable)
Move Right    → RIGHT ARROW (rebindable)
Move Down     → DOWN ARROW (rebindable)
Rotate        → UP ARROW (rebindable)
Hard Drop     → SPACEBAR (rebindable)

Access control customization from Settings → Controls menu.

## Theme System

### Available Themes

**Classic Theme**
- Gray background with cyan outline
- Traditional Tetris aesthetic
- Black text for contrast

**Starry Theme**
- Dark purple board with mystical appearance
- Violet highlights and glowing outline
- Atmospheric gaming experience

**Dark Theme** (Default)
- Minimalist dark gray background
- Clean black board
- White text for maximum contrast
- Modern, professional appearance

### Theme Switching
- Select from settings menu
- Quick toggle with keys 1, 2, 3 during gameplay
- Affects all UI elements including board, preview, and text

## Game States

- **Main Menu** - Navigation and start game
- **Settings** - Theme and control configuration
- **Playing** - Active gameplay
- **Game Over** - Score display with replay/quit options
- **Name Input** - Player name submission for leaderboard

## Code Refactoring

### Clean Architecture
- Removed magic numbers and replaced with named constants
- Clear, descriptive variable and function naming
- Organized into logical class hierarchy
- Separated concerns: UI, game logic, rendering

### Maintainability
- Comprehensive code documentation
- Reduced code duplication
- Reusable utility functions
- Easy to extend and modify