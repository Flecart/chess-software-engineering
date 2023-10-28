
from .figures import Pawn, Rook, Knight, Bishop, Queen, King
from .enums import Colors

BISHOP_MOVES = (1, 1), (-1, -1), (1, -1), (-1, 1)
KNIGHT_MOVES = (1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)
ROOK_MOVES = (1, 0), (-1, 0), (0, 1), (0, -1)
QUEEN_MOVES = BISHOP_MOVES + ROOK_MOVES
KING_MOVES = QUEEN_MOVES

FIGURES_MAP = {
    'p': (Pawn, Colors.BLACK),
    'r': (Rook, Colors.BLACK),
    'n': (Knight, Colors.BLACK),
    'b': (Bishop, Colors.BLACK),
    'q': (Queen, Colors.BLACK),
    'k': (King, Colors.BLACK),
    'P': (Pawn, Colors.WHITE),
    'R': (Rook, Colors.WHITE),
    'N': (Knight, Colors.WHITE),
    'B': (Bishop, Colors.WHITE),
    'Q': (Queen, Colors.WHITE),
    'K': (King, Colors.WHITE),
}
