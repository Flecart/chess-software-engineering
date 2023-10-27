from .figure import Figure
from ..enums import Pieces

class Rook(Figure):
    _symbol = 'R'
    kind = Pieces.ROOK

    def updateMoves(self):
        from ..const import ROOK_MOVES
        self._moves = self.getLineMoves(ROOK_MOVES)
