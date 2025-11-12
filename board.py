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

