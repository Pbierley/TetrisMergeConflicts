import pygame
from constants import COLORS, BLACK, WHITE, WINDOW_SIZE


def draw_board(screen, board, start_x, start_y, preview_x, preview_y, block_size, theme):
    """Draw the game board"""
    screen.fill(theme["background"])

    # Draw box for preview piece
    preview_rect = pygame.Rect(
        preview_x,
        preview_y - 8,
        200, 100
    )
    pygame.draw.rect(screen, theme["next"], preview_rect)
    # Label for the next piece
    font = pygame.font.SysFont('Calibri', 20, True, False)
    next_text = font.render("Next Piece:", True, theme["text"])
    screen.blit(next_text, [preview_x - 20, preview_y - 30])
    
    # Draw the board background
    playfield_rect = pygame.Rect(
        start_x, 
        start_y, 
        board.width * block_size, 
        board.height * block_size
    )
    pygame.draw.rect(screen, theme["board"], playfield_rect)

    # Draw the board outline
    border_rect = pygame.Rect(
        start_x - 8, 
        start_y, 
        board.width * block_size + 16, 
        board.height * block_size + 8
    )
    pygame.draw.rect(screen, theme["outline"], border_rect, 8)



    for i in range(board.height):
        for j in range(board.width):
            x = start_x + block_size * j
            y = start_y + block_size * i

            # Draw placed pieces
            if board.grid[i][j] > 0:
                pygame.draw.rect(screen, COLORS[board.grid[i][j]],
                               [x + 1, y + 1, block_size - 2, block_size - 2])


def draw_piece(screen, piece, start_x, start_y, block_size):
    """Draw the current falling piece"""
    if not piece:
        return
        
    blocks = piece.get_blocks()
    
    for i in range(4):
        for j in range(4):
            if i * 4 + j in blocks:
                x = start_x + block_size * (j + piece.x) + 1
                y = start_y + block_size * (i + piece.y) + 1
                
                pygame.draw.rect(screen, COLORS[piece.color],
                               [x, y, block_size - 2, block_size - 2])


def draw_leaderboard(screen, leaderboard_data, x, y, theme):
    """Draw the leaderboard on screen"""
    font_title = pygame.font.SysFont('Calibri', 20, True, False)
    font_entry = pygame.font.SysFont('Calibri', 16, False, False)
    
    # Draw title
    title_text = font_title.render("Leaderboard:", True, theme["text"])
    screen.blit(title_text, [x, y])
    
    # Draw entries
    for i, entry in enumerate(leaderboard_data):
        entry_y = y + 25 + (i * 20)
        entry_text = font_entry.render(f"{i+1}. {entry['name']}: {entry['score']}", True, theme["text"])
        screen.blit(entry_text, [x, entry_y])


def draw_name_input_screen(screen, game):
    """Draw the name input screen when game is over"""
    # Semi-transparent overlay
    overlay = pygame.Surface(WINDOW_SIZE)
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont('Calibri', 48, True, False)
    font_medium = pygame.font.SysFont('Calibri', 32, True, False)
    font_small = pygame.font.SysFont('Calibri', 24, False, False)
    
    # Game Over text
    game_over_text = font_large.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, [150, 100])
    
    # Score text
    score_text = font_medium.render(f"Your Score: {game.score}", True, WHITE)
    screen.blit(score_text, [180, 160])
    
    # Name input prompt
    prompt_text = font_medium.render("Enter your name:", True, WHITE)
    screen.blit(prompt_text, [170, 220])
    
    # Name input box
    input_box = pygame.Rect(150, 270, 300, 40)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    
    # Display current name input
    name_text = font_medium.render(game.player_name, True, BLACK)
    screen.blit(name_text, [input_box.x + 5, input_box.y + 5])
    
    # Instructions
    instruction_text = font_small.render("Press ENTER to save score", True, WHITE)
    screen.blit(instruction_text, [180, 330])
    
    instruction_text2 = font_small.render("Press ESC to quit without saving", True, WHITE)
    screen.blit(instruction_text2, [155, 360])

