import pygame
import random
from supabase import create_client, Client


SUPABASE_URL="https://ddafhennccnnqlzdaxer.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkYWZoZW5uY2NubnFsemRheGVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzkxMjUsImV4cCI6MjA3NDMxNTEyNX0.iBn49djWQBUkoyJ6dXFD9g02oNibyhU8XRCEpNFQCtM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        self.state = "playing"  # "playing", "gameover", or "entering_name"
        self.score_saved = False  # Track if score has been saved to database
        self.player_name = ""  # Store the player's name input
        self.spawn_new_piece()
        self.sounds = sounds

    def spawn_new_piece(self):
        """Create a new piece at the top"""
        if self.next_piece is None:
            self.next_piece = Piece()

        self.current_piece = self.next_piece
        self.next_piece = Piece()
        
        # Check if game is over (can't place new piece)
        if self.board.collides(self.current_piece):
            self.state = "entering_name"
    
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


def get_leaderboard():
    """Fetch top 5 scores from the leaderboard"""
    try:
        response = (
            supabase.table("Leaderboard")
            .select("name, score")
            .order("score", desc=True)
            .limit(5)
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []


def draw_leaderboard(screen, leaderboard_data, x, y):
    """Draw the leaderboard on screen"""
    font_title = pygame.font.SysFont('Calibri', 20, True, False)
    font_entry = pygame.font.SysFont('Calibri', 16, False, False)
    
    # Draw title
    title_text = font_title.render("Leaderboard:", True, BLACK)
    screen.blit(title_text, [x, y])
    
    # Draw entries
    for i, entry in enumerate(leaderboard_data):
        entry_y = y + 25 + (i * 20)
        entry_text = font_entry.render(f"{i+1}. {entry['name']}: {entry['score']}", True, BLACK)
        screen.blit(entry_text, [x, entry_y])


def save_score_to_database(name, score):
    """Save the player's score to the database"""
    try:
        response = (
            supabase.table("Leaderboard")
            .insert({"name": name, "score": score})
            .execute()
        )
        print(f"Score {score} for player '{name}' saved to database!")
        return True
    except Exception as e:
        print(f"Error saving score: {e}")
        return False


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
        'placed': pygame.mixer.Sound('./assets/bloop-short.MP3'),
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
    
    # Fetch leaderboard at start
    leaderboard_data = get_leaderboard()
    
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
                if game.state == "playing":
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
                
                elif game.state == "entering_name":
                    if event.key == pygame.K_RETURN:
                        # Save score if name is entered
                        if game.player_name.strip():
                            if save_score_to_database(game.player_name.strip(), game.score):
                                leaderboard_data = get_leaderboard()  # Refresh leaderboard
                                game.score_saved = True
                            game.state = "gameover"
                        else:
                            # Don't allow empty names
                            pass
                    elif event.key == pygame.K_ESCAPE:
                        # Skip saving and go to game over screen
                        game.state = "gameover"
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove last character
                        game.player_name = game.player_name[:-1]
                    else:
                        # Add character to name (limit to reasonable length)
                        if len(game.player_name) < 20:
                            if event.unicode.isprintable():
                                game.player_name += event.unicode
                
                elif game.state == "gameover":
                    if event.key == pygame.K_q:
                        done = True
            
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False
        
        # Draw everything
        draw_board(screen, game.board, start_x, start_y, block_size)
        
        if game.state == "playing":
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
        
        # Draw leaderboard
        draw_leaderboard(screen, leaderboard_data, 350, 200)
        
        # Draw name input screen
        if game.state == "entering_name":
            draw_name_input_screen(screen, game)
        
        # Draw game over screen
        elif game.state == "gameover":
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