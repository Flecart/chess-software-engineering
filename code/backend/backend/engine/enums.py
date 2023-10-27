from enum import IntEnum

class Pieces(IntEnum):
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Colors(IntEnum):
    WHITE = 0
    BLACK = 1

class EndReasons(IntEnum):
    CHECKMATE = 1
    DRAW = 2
    RESIGN = 3
    TIME = 4
