from enum import StrEnum

START_POSITION_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
KRIEGSPIEL_INVALID_MOVE = "Illegal move."
MAX_KRIEGSPIEL_MOVES = 3


class Color(StrEnum):
    WHITE = "white"
    BLACK = "black"

class GameTypes(StrEnum):
    DARK_CHESS = "dark_chess"
    # TODO: add other game types
