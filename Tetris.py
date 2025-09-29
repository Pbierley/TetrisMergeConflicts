import pygame
import random

# Constants
COLORS = (
    (0, 0, 0),        # Black (empty)
    (120, 37, 179),   # Purple
    (100, 179, 179),  # Cyan
    (80, 34, 22),     # Brown
    (80, 134, 22),    # Green
    (180, 34, 22),    # Red
    (180, 34, 122),   # Pink
)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

PIECES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[4, 5, 9, 10], [2, 6, 5, 9]],  # Z
    [[6, 7, 9, 10], [1, 5, 6, 10]], # S
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # T
    [[1, 2, 5, 6]]  # O
]

WINDOW_SIZE = (600, 500)


class Piece:
    """Represents a Tetris piece with its position, rotation, and type"""
    
    def __init__(self, x=3, y=0):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(PIECES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0
    
    def get_blocks(self):
        """Get the current block positions"""
        return PIECES[self.type][self.rotation]
    
    def move(self, dx, dy, board):
        """Try to move the piece. Returns True if successful."""
        old_x, old_y = self.x, self.y
        self.x += dx
        self.y += dy
        
        if board.collides(self):
            self.x, self.y = old_x, old_y
            return False
        return True
    
    def rotate(self, board):
        """Try to rotate the piece. Returns True if successful."""
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(PIECES[self.type])
        
        if board.collides(self):
            self.rotation = old_rotation
            return False
        return True
    
    def drop_to_bottom(self, board):
        """Drop the piece to the bottom"""
        while self.move(0, 1, board):
            pass


class Board:
    """Represents the game board/playing field"""
    
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    def collides(self, piece):
        """Check if piece collides with board boundaries or placed pieces"""
        blocks = piece.get_blocks()
        
        for i in range(4):
            for j in range(4):
                if i * 4 + j in blocks:
                    new_y = i + piece.y
                    new_x = j + piece.x
                    
                    # Check boundaries and collisions
                    if (new_y >= self.height or 
                        new_x >= self.width or 
                        new_x < 0 or 
                        (new_y >= 0 and self.grid[new_y][new_x] > 0)):
                        return True
        return False
    
    def place_piece(self, piece):
        """Place a piece on the board (freeze it)"""
        blocks = piece.get_blocks()
        
        for i in range(4):
            for j in range(4):
                if i * 4 + j in blocks:
                    board_y = i + piece.y
                    board_x = j + piece.x
                    if board_y >= 0:  # Don't place blocks above visible area
                        self.grid[board_y][board_x] = piece.color
    
    def clear_lines(self):
        """Clear completed lines and return number of lines cleared"""
        lines_cleared = 0
        
        # Check from bottom to top
        row = self.height - 1
        while row >= 0:
            if self._is_line_full(row):
                self._remove_line(row)
                lines_cleared += 1
                # Don't decrement row, check same position again
            else:
                row -= 1
                
        return lines_cleared
    
    def _is_line_full(self, row):
        """Check if a row is completely filled"""
        return all(cell > 0 for cell in self.grid[row])
    
    def _remove_line(self, row_to_remove):
        """Remove a line and shift everything down"""
        del self.grid[row_to_remove]
        self.grid.insert(0, [0] * self.width)


class Game:
    """Manages the game state, score, and piece spawning"""
    
    def __init__(self, width=10, height=20, sounds=None):
        self.board = Board(width, height)
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.state = "playing"  # "playing" or "gameover"
        self.spawn_new_piece()
        self.sounds = sounds

    def spawn_new_piece(self):
        """Create a new piece at the top"""
        if self.next_piece is  None:
            self.next_piece = Piece()

        self.current_piece = self.next_piece
        self.next_piece = Piece()
        
        # Check if game is over (can't place new piece)
        if self.board.collides(self.current_piece):
            self.state = "gameover"
    
    def move_piece(self, dx, dy):
        """Move the current piece"""
        if self.state == "playing" and self.current_piece:
            return self.current_piece.move(dx, dy, self.board)
        return False
    
    def rotate_piece(self):
        """Rotate the current piece"""
        if self.state == "playing" and self.current_piece:
            return self.current_piece.rotate(self.board)
        return False
    
    def drop_piece(self):
        """Drop current piece to bottom and freeze it"""
        if self.state == "playing" and self.current_piece:
            self.current_piece.drop_to_bottom(self.board)
            self.freeze_current_piece()
    
    def tick(self):
        """Game tick - try to move piece down"""
        if self.state == "playing" and self.current_piece:
            if not self.current_piece.move(0, 1, self.board):
                self.freeze_current_piece()
    
    def freeze_current_piece(self):
        """Freeze the current piece and handle line clearing"""
        if self.current_piece:
            # Play placed sound
            if self.sounds:
                self.sounds['placed'].play()
            self.board.place_piece(self.current_piece)
            lines_cleared = self.board.clear_lines()

            # Play line clear sound
            if self.sounds and lines_cleared > 0:
                self.sounds['line_clear'].play()
            
            # Update score
            if lines_cleared > 0:
                self.score += lines_cleared ** 2
            
            self.spawn_new_piece()


def draw_board(screen, board, start_x, start_y, block_size):
    """Draw the game board"""
    screen.fill(WHITE)
    
    for i in range(board.height):
        for j in range(board.width):
            x = start_x + block_size * j
            y = start_y + block_size * i
            
            # Draw grid
            pygame.draw.rect(screen, GRAY, [x, y, block_size, block_size], 1)
            
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



def main():
    # Initialize pygame
    pygame.mixer.pre_init()
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Play song
    pygame.mixer.music.load('./assets/intro-theme.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # Load sound effects early
    sounds = {
        'placed': pygame.mixer.Sound('./assets/bloop-short.mp3'),
        'line_clear': pygame.mixer.Sound('./assets/debris-break.mp3'),
    }
    
    # Game settings
    start_x, start_y = 100, 60
    block_size = 20
    fps = 25
    
    # Game state
    game = Game(sounds=sounds)
    counter = 0
    pressing_down = False
    done = False
    
    while not done:
        counter += 1
        if counter > 100000:
            counter = 0
        
        # Automatic piece dropping
        if counter % (fps // 2) == 0 or pressing_down:
            if game.state == "playing":
                game.tick()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_SPACE:
                    game.drop_piece()
                elif event.key == pygame.K_DOWN:
                    pressing_down = True
                elif event.key == pygame.K_q and game.state == "gameover":
                    done = True
            
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False
        
        # Draw everything
        draw_board(screen, game.board, start_x, start_y, block_size)
        draw_piece(screen, game.current_piece, start_x, start_y, block_size)
        
        # Box to show the next piece
        preview_x, preview_y = 350, 100
        draw_piece(screen, game.next_piece, preview_x, preview_y, block_size)

        # Label for the next piece
        font = pygame.font.SysFont('Calibri', 20, True, False)
        next_text = font.render("Next Piece:", True, BLACK)
        screen.blit(next_text, [preview_x - 20, preview_y - 30])

        # Draw score
        font = pygame.font.SysFont('Calibri', 25, True, False)
        score_text = font.render(f"Score: {game.score}", True, BLACK)
        screen.blit(score_text, [10, 10])
        
        # Draw game over screen
        if game.state == "gameover":
            font_large = pygame.font.SysFont('Calibri', 65, True, False)
            game_over_text = font_large.render("Game Over", True, (255, 125, 0))
            quit_text = font_large.render("Press Q to Quit", True, (255, 215, 0))
            screen.blit(game_over_text, [20, 200])
            screen.blit(quit_text, [25, 265])
        
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()


if __name__ == "__main__":
    main()