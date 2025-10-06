# test_tetris.py
import sys
import types
import importlib
import builtins
import pytest

# ---------- Minimal stubs so importing tetris.py is safe (no SDL, no network) ----------
class _DummySound:
    def __init__(self, *_a, **_k):
        self.played = False
    def play(self):
        self.played = True

def _make_dummy_pygame():
    pg = types.ModuleType("pygame")
    # constants used in tetris (keep for safety even if not used in tests)
    pg.K_UP = 273; pg.K_DOWN = 274; pg.K_LEFT = 276; pg.K_RIGHT = 275
    pg.K_SPACE = 32; pg.K_q = 113
    pg.QUIT = 12; pg.KEYDOWN = 2; pg.KEYUP = 3

    # submodules
    mixer = types.SimpleNamespace(
        pre_init=lambda *a, **k: None,
        Sound=lambda *a, **k: _DummySound(),
        music=types.SimpleNamespace(load=lambda *a, **k: None,
                                    set_volume=lambda *a, **k: None,
                                    play=lambda *a, **k: None)
    )
    pg.mixer = mixer

    # used by draw functions (which we don't call), but keep stubs
    def _noop(*_a, **_k): pass
    pg.init = _noop
    pg.display = types.SimpleNamespace(set_mode=lambda *a, **k: None,
                                       set_caption=_noop,
                                       flip=_noop)
    pg.time = types.SimpleNamespace(Clock=lambda: types.SimpleNamespace(tick=_noop))
    pg.event = types.SimpleNamespace(get=lambda: [])
    pg.font = types.SimpleNamespace(SysFont=lambda *a, **k: types.SimpleNamespace(render=lambda *a, **k: None))
    pg.draw = types.SimpleNamespace(rect=_noop)
    pg.Surface = object
    return pg

def _make_dummy_supabase():
    sb = types.ModuleType("supabase")
    class _DummyTable:
        def insert(self, *a, **k): return self
        def execute(self): return {"status": "ok"}
    class _DummyClient:
        def table(self, *a, **k): return _DummyTable()
    def create_client(*_a, **_k): return _DummyClient()
    sb.create_client = create_client
    sb.Client = object
    return sb

@pytest.fixture(scope="session")
def tetris_module():
    # Inject stubs before import
    sys.modules.setdefault("pygame", _make_dummy_pygame())
    sys.modules.setdefault("supabase", _make_dummy_supabase())
    # (Re)import fresh to ensure stubs are used
    if "tetris" in sys.modules:
        del sys.modules["tetris"]
    tetris = importlib.import_module("tetris")
    return tetris

# ---------- Helpers ----------
class DummySound:
    def __init__(self): self.played = False
    def play(self): self.played = True

def make_silent_sounds():
    return {"placed": DummySound(), "line_clear": DummySound()}

def force_piece(t, p, *, type_idx=None, rotation=None, x=None, y=None, color=1):
    if type_idx is not None: p.type = type_idx
    if rotation is not None: p.rotation = rotation % len(t.PIECES[p.type])
    if x is not None: p.x = x
    if y is not None: p.y = y
    p.color = color
    return p

# ---------- Tests: Piece ----------
def test_piece_moves_without_collision(tetris_module):
    t = tetris_module
    b = t.Board(10, 20)
    p = force_piece(t, t.Piece(), type_idx=6, x=3, y=0)  # O piece
    ok = p.move(1, 0, b)
    assert ok is True
    assert (p.x, p.y) == (4, 0)

def test_piece_move_blocked_by_right_wall(tetris_module):
    t = tetris_module
    b = t.Board(10, 20)
    # O piece occupies j in {1,2}; placing at x=8 should block moving right
    p = force_piece(t, t.Piece(), type_idx=6, x=b.width - 2, y=0)
    ok = p.move(1, 0, b)
    assert ok is False
    assert (p.x, p.y) == (b.width - 2, 0)

def test_piece_rotation_reverts_on_collision(tetris_module):
    t = tetris_module
    b = t.Board(10, 20)
    # I piece vertical at x=8; rotating to horizontal would exceed width
    p = force_piece(t, t.Piece(), type_idx=0, rotation=0, x=b.width - 2, y=0)
    prev_rot = p.rotation
    ok = p.rotate(b)
    assert ok is False
    assert p.rotation == prev_rot  # reverted

def test_piece_drop_to_bottom_stops_above_floor(tetris_module):
    t = tetris_module
    b = t.Board(10, 20)
    # Vertical I ends with i in {0..3}. Max y so i+ y <= 19 -> y=16
    p = force_piece(t, t.Piece(), type_idx=0, rotation=0, x=0, y=0)
    p.drop_to_bottom(b)
    assert p.y == b.height - 4  # 20 - 4 = 16

# ---------- Tests: Board ----------
def test_board_place_piece_and_clear_one_line(tetris_module):
    t = tetris_module
    b = t.Board(10, 20)

    # Fill bottom row except two cells (at x=4,5) to be completed by an O piece
    b.grid[-1] = [1] * 10
    b.grid[-1][4] = 0
    b.grid[-1][5] = 0

    # Place O piece (blocks at (x+1,y) (x+2,y) and same for y+1), so set y=18
    p = force_piece(t, t.Piece(), type_idx=6, x=4, y=b.height - 2, color=2)
    assert b.collides(p) is False

    b.place_piece(p)
    lines = b.clear_lines()
    assert lines == 1
    # After clearing, bottom row should be zeros (a new empty row inserted)
    assert b.grid[0] == [0] * b.width  # new row at top
    assert b.grid[-1] == [0] * b.width  # bottom row now empty

def test_board_collides_with_existing_blocks(tetris_module):
    t = tetris_module
    b = t.Board(10, 20)
    b.grid[10][5] = 3  # place a block
    p = force_piece(t, t.Piece(), type_idx=6, x=4, y=9)  # O piece will overlap (10,5)
    assert b.collides(p) is True

# ---------- Tests: Game ----------
def test_game_tick_freezes_on_floor_and_plays_sound(tetris_module):
    t = tetris_module
    sounds = make_silent_sounds()
    g = t.Game(width=10, height=20, sounds=sounds)

    # Force current piece to O just above the floor so a single tick freezes it
    g.current_piece = force_piece(t, t.Piece(), type_idx=6, x=4, y=18)
    # Ensure no collision yet, but moving down would collide -> freeze
    assert g.board.collides(g.current_piece) is False

    g.tick()  # should attempt to move down, fail, then freeze/place/spawn
    assert sounds["placed"].played is True
    # Score unchanged (no line clear), and a new piece should be active
    assert g.score == 0
    assert g.current_piece is not None
    assert g.state == "playing"

def test_game_scores_on_single_line_clear(tetris_module):
    t = tetris_module
    sounds = make_silent_sounds()
    g = t.Game(width=10, height=20, sounds=sounds)

    # Prepare board: bottom row filled except x=4 and x=5
    g.board.grid[-1] = [1] * g.board.width
    g.board.grid[-1][4] = 0
    g.board.grid[-1][5] = 0

    # Force an O piece that will complete the row and freeze on tick
    g.current_piece = force_piece(t, t.Piece(), type_idx=6, x=4, y=18)
    g.tick()

    assert g.score == 1  # (1 line) ** 2
    assert sounds["line_clear"].played is True

def test_game_over_when_new_piece_cannot_spawn(tetris_module):
    t = tetris_module
    sounds = make_silent_sounds()
    g = t.Game(width=10, height=20, sounds=sounds)

    # Fill the top 4 rows to guarantee collision for any spawn position
    for r in range(4):
        g.board.grid[r] = [1] * g.board.width

    # Force a respawn
    g.spawn_new_piece()
    assert g.state == "gameover"
