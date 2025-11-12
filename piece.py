import random
from constants import PIECES, COLORS


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

