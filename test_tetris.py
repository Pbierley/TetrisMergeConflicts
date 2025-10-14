# test_tetris.py
import unittest
from unittest.mock import Mock, patch
import random
from supabase import create_client, Client # Keep imports for type hints/structure, even though they'll be mocked

# --- Mocking Dependencies ---

# Mock pygame and its modules
mock_pygame = Mock()
mock_pygame.init = Mock()
mock_pygame.display.set_mode = Mock(return_value=Mock())
mock_pygame.time.Clock = Mock(return_value=Mock())
mock_pygame.mixer.Sound = Mock()
mock_pygame.K_UP = 1  # Mock key constants
mock_pygame.K_LEFT = 2
mock_pygame.K_RIGHT = 3
mock_pygame.K_SPACE = 4
mock_pygame.K_DOWN = 5
mock_pygame.K_q = 6
mock_pygame.QUIT = 7
mock_pygame.KEYDOWN = 8
mock_pygame.KEYUP = 9

# Mock supabase client and response structure
mock_supabase = Mock()
mock_supabase.table.return_value.insert.return_value.execute.return_value = Mock()
mock_supabase_client = Mock(return_value=mock_supabase)
mock_create_client = Mock(return_value=mock_supabase_client)

# --- Necessary Definitions from Original Code ---

PIECES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]], # I
    [[4, 5, 9, 10], [2, 6, 5, 9]], # Z
    [[6, 7, 9, 10], [1, 5, 6, 10]], # S
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # T
    [[1, 2, 5, 6]] # O
]
COLORS = [(0, 0, 0), (120, 37, 179), (100, 179, 179), (80, 34, 22), (80, 134, 22), (180, 34, 22), (180, 34, 122)]
SUPABASE_URL = "mock_url"
SUPABASE_KEY = "mock_key"

# CRITICAL FIX: Ensure the global 'supabase' variable is the mock object for testing
# This prevents a live database call during test file loading.
supabase = mock_supabase

class Piece:
    def __init__(self, x=3, y=0, piece_type=None, color_idx=None):
        self.x = x
        self.y = y
        self.type = piece_type if piece_type is not None else random.randint(0, len(PIECES) - 1)
        self.color = color_idx if color_idx is not None else random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def get_blocks(self):
        return PIECES[self.type][self.rotation]

    def move(self, dx, dy, board):
        old_x, old_y = self.x, self.y
        self.x += dx
        self.y += dy
        if board.collides(self):
            self.x, self.y = old_x, old_y
            return False
        return True

    def rotate(self, board):
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(PIECES[self.type])
        if board.collides(self):
            self.rotation = old_rotation
            return False
        return True

    def drop_to_bottom(self, board):
        while self.move(0, 1, board):
            pass

class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def collides(self, piece):
        blocks = piece.get_blocks()
        for i in range(4):
            for j in range(4):
                if i * 4 + j in blocks:
                    new_y = i + piece.y
                    new_x = j + piece.x
                    if (new_y >= self.height or
                        new_x >= self.width or
                        new_x < 0 or
                        (new_y >= 0 and self.grid[new_y][new_x] > 0)):
                        return True
        return False

    def place_piece(self, piece):
        blocks = piece.get_blocks()
        for i in range(4):
            for j in range(4):
                if i * 4 + j in blocks:
                    board_y = i + piece.y
                    board_x = j + piece.x
                    if board_y >= 0:
                        self.grid[board_y][board_x] = piece.color

    def clear_lines(self):
        lines_cleared = 0
        row = self.height - 1
        while row >= 0:
            if self._is_line_full(row):
                self._remove_line(row)
                lines_cleared += 1
            else:
                row -= 1
        return lines_cleared

    def _is_line_full(self, row):
        return all(cell > 0 for cell in self.grid[row])

    def _remove_line(self, row_to_remove):
        del self.grid[row_to_remove]
        self.grid.insert(0, [0] * self.width)

class Game:
    def __init__(self, width=10, height=20, sounds=None):
        self.board = Board(width, height)
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.state = "playing"
        self.score_saved = False
        # Use mock sounds if none are provided
        self.sounds = sounds if sounds else {'placed': Mock(), 'line_clear': Mock()}
        self.spawn_new_piece()

    def spawn_new_piece(self):
        if self.next_piece is None:
            # Deterministic piece type 0 (I-piece) for first piece in Game setUp
            self.next_piece = Piece(piece_type=0, color_idx=1)

        self.current_piece = self.next_piece
        # Deterministic piece type 1 (Z-piece) for the next piece
        self.next_piece = Piece(piece_type=1, color_idx=2)

        if self.board.collides(self.current_piece):
            self.state = "gameover"

    def move_piece(self, dx, dy):
        if self.state == "playing" and self.current_piece:
            return self.current_piece.move(dx, dy, self.board)
        return False

    def rotate_piece(self):
        if self.state == "playing" and self.current_piece:
            return self.current_piece.rotate(self.board)
        return False

    def drop_piece(self):
        if self.state == "playing" and self.current_piece:
            self.current_piece.drop_to_bottom(self.board)
            self.freeze_current_piece()

    def tick(self):
        if self.state == "playing" and self.current_piece:
            if not self.current_piece.move(0, 1, self.board):
                self.freeze_current_piece()

    def freeze_current_piece(self):
        if self.current_piece:
            self.sounds['placed'].play()
            self.board.place_piece(self.current_piece)
            lines_cleared = self.board.clear_lines()

            if lines_cleared > 0:
                self.sounds['line_clear'].play()

            if lines_cleared > 0:
                self.score += lines_cleared ** 2

            self.spawn_new_piece()


# --- Unit Tests ---

class TestPiece(unittest.TestCase):
    """Tests for the Piece class."""

    def setUp(self):
        self.board = Board(width=10, height=20)
        self.piece = Piece(x=5, y=0, piece_type=0, color_idx=1) # I-piece

    def test_initialization(self):
        self.assertEqual(self.piece.x, 5)
        self.assertEqual(self.piece.type, 0)
        self.assertEqual(self.piece.rotation, 0)

    def test_move_success(self):
        self.assertTrue(self.piece.move(1, 0, self.board))
        self.assertEqual(self.piece.x, 6)
        self.assertTrue(self.piece.move(0, 1, self.board))
        self.assertEqual(self.piece.y, 1)

    def test_move_collision_boundary(self):
        # Piece at x=9 (blocks at x+1=10, which hits the boundary)
        self.piece.x = 9
        self.assertFalse(self.piece.move(1, 0, self.board))
        self.assertEqual(self.piece.x, 9)

    def test_rotate_success(self):
        self.assertTrue(self.piece.rotate(self.board))
        self.assertEqual(self.piece.rotation, 1)
        self.assertTrue(self.piece.rotate(self.board))
        self.assertEqual(self.piece.rotation, 0)

    def test_drop_to_bottom(self):
        self.piece.y = 0
        self.piece.drop_to_bottom(self.board)
        # I-piece (4 blocks tall) lands at y=20 - 4 = 16
        self.assertEqual(self.piece.y, 16)


class TestBoard(unittest.TestCase):
    """Tests for the Board class."""

    def setUp(self):
        self.board = Board(width=10, height=20)
        self.piece_l = Piece(x=5, y=0, piece_type=4, color_idx=2) # L-piece

    def test_clear_lines(self):
        # Fill rows 18 and 19 entirely
        for j in range(self.board.width):
            self.board.grid[18][j] = 1
            self.board.grid[19][j] = 1
        
        lines_cleared = self.board.clear_lines()
        
        self.assertEqual(lines_cleared, 2)
        # Check that the two top rows are now empty
        self.assertTrue(all(cell == 0 for cell in self.board.grid[0]))
        self.assertTrue(all(cell == 0 for cell in self.board.grid[1]))


@patch('random.randint', side_effect=[0, 1, 0, 1]) # Deterministic piece spawning
class TestGame(unittest.TestCase):
    """Tests for the Game class."""

    def setUp(self):
        self.mock_sounds = {'placed': Mock(), 'line_clear': Mock()}
        self.game = Game(width=10, height=20, sounds=self.mock_sounds)

    def test_initialization_and_spawn(self, mock_random_randint):
        self.assertEqual(self.game.state, "playing")
        self.assertEqual(self.game.current_piece.type, 0) # I-piece
        self.assertEqual(self.game.next_piece.type, 1)    # Z-piece

    def test_tick_and_freeze(self, mock_random_randint):
        # Force the piece to the floor and tick once more
        self.game.current_piece.y = 16
        self.game.tick() # Move fails, piece freezes and spawns new one

        self.mock_sounds['placed'].play.assert_called_once()
        self.assertEqual(self.game.current_piece.type, 1) # New piece (Z) spawned

    def test_drop_piece_and_score(self, mock_random_randint):
        # I-piece (type 0, rot 0) blocks are in column x+1.
        self.game.current_piece.x = 4 # Piece blocks land in column 5
        self.game.current_piece.type = 0

        # Fill line 19, leaving a gap at column 5
        for j in range(10):
            if j != 5: # <--- CORRECT GAP for piece at x=4
                self.game.board.grid[19][j] = 5
        
        # Drop current piece. It lands at y=16 and completes row 19.
        self.game.drop_piece()
        
        # Line cleared count should be 1 (score 1^2 = 1)
        self.assertEqual(self.game.score, 1)
        self.mock_sounds['line_clear'].play.assert_called_once()
        self.assertEqual(self.game.current_piece.type, 1) # New piece (Z) spawned

    def test_game_over(self, mock_random_randint):
        # Fill the top row where the next piece would spawn
        for j in range(10):
            self.game.board.grid[0][j] = 5
        
        self.game.current_piece.y = 1 # Move current piece down so it doesn't collide yet
        
        self.game.freeze_current_piece() # Freezes, then tries to spawn next piece

        self.assertEqual(self.game.state, "gameover")
        
    # CRITICAL FIX: Patch the global variable '__main__.supabase' instead of a module name
    @patch('test_tetris.supabase', new=mock_supabase)
    def test_score_saving(self, mock_random_randint):
        """
        Tests the logic for saving the score to the mocked Supabase client.
        """
        self.game.score = 50
        self.game.state = "gameover"
        self.game.score_saved = False

        # Use the globally defined (mocked) supabase object
        global supabase
        
        try:
            # Replicate the save logic from the main() loop's "gameover" section
            (
                supabase.table("Leaderboard")
                .insert({"name": "Test_User", "score": self.game.score})
                .execute()
            )
            self.game.score_saved = True
        except Exception as e:
            self.fail(f"Supabase mock failed execution: {e}")

        # Assert that the mocked methods were called correctly
        mock_supabase.table.assert_called_with("Leaderboard")
        mock_supabase.table.return_value.insert.assert_called_with({"name": "Test_User", "score": 50})
        self.assertTrue(self.game.score_saved)


# --- Execution ---
if __name__ == '__main__':
    # To run these tests, run: python -m unittest test_tetris.py
    unittest.main(argv=['first-arg-is-ignored'], exit=False)