from .figure import Figure
from ..enums import Pieces

class Queen(Figure):
    _symbol = 'Q'
    kind = Pieces.QUEEN

    def updateMoves(self):
        from ..const import QUEEN_MOVES
        self._moves = self.getLineMoves(QUEEN_MOVES)
