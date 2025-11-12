# Constants and configuration

# Supabase configuration
SUPABASE_URL = "https://ddafhennccnnqlzdaxer.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkYWZoZW5uY2NubnFsemRheGVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzkxMjUsImV4cCI6MjA3NDMxNTEyNX0.iBn49djWQBUkoyJ6dXFD9g02oNibyhU8XRCEpNFQCtM"

# Colors
COLORS = (
    (0, 0, 0),        # Black (empty)
    (0, 240, 240),     # Cyan
    (240, 240, 0),     # Yellow
    (128, 0, 128),     # Purple
    (0, 240, 0),       # Green
    (240, 0, 0),       # Red
    (0, 0, 240),       # Blue
    (255, 127, 0)     # Orange
)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Tetris pieces (rotations)
PIECES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[4, 5, 9, 10], [2, 6, 5, 9]],  # Z
    [[6, 7, 9, 10], [1, 5, 6, 10]], # S
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # T
    [[1, 2, 5, 6]]  # O
]

# Themes
THEMES = {
    "Classic": {
        "background": (121, 121, 121),
        "board": (0, 0, 0),
        "next": BLACK,
        "outline": (0, 242, 242),
        "text": BLACK
    },
    "Starry": {
        "background": BLACK,
        "board": (31, 31, 88),
        "next": (89, 79, 126),
        "outline": (143, 128, 179),
        "text": (133, 120, 158)
    },
    "Dark": {
        "background": (20, 20, 20),
        "board": BLACK,
        "next": BLACK,
        "outline": (60, 60, 60),
        "text": (255, 255, 255)
    }
}

WINDOW_SIZE = (600, 500)

