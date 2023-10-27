from .figure import Figure
from ..enums import Pieces
from ..errors import OutOfBoardError


class Knight(Figure):
    _symbol = 'N'
    kind = Pieces.KNIGHT

    def updateMoves(self):
        from ..const import KNIGHT_MOVES
        moves = []
        for dx, dy in (KNIGHT_MOVES):
            x = self.x + dx
            y = self.y + dy
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                continue
            if not fig or self.isEnemy(fig):
                moves.append((x, y))
        self._moves = moves