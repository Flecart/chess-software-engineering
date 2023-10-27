from .figure import Figure
from ..enums import Pieces

class Bishop(Figure):
    _symbol: str = 'B'
    kind: Pieces = Pieces.BISHOP

    def updateMoves(self):
        from ..const import BISHOP_MOVES
        self._moves = self.getLineMoves(BISHOP_MOVES)