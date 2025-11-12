from board import Board
from piece import Piece
from constants import THEMES


class Game:
    """Manages the game state, score, and piece spawning"""

    def __init__(self, width=10, height=20, sounds=None, theme_name="Dark"):
        self.board = Board(width, height)
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.state = "playing"  # "playing", "gameover", or "entering_name"
        self.score_saved = False  # Track if score has been saved to database
        self.player_name = ""  # Store the player's name input
        self.spawn_new_piece()
        self.sounds = sounds
        self.set_theme(theme_name)
    
    def set_theme(self, theme_name):
        """Set theme for the game"""
        self.theme_name = theme_name
        self.theme = THEMES[theme_name]

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

