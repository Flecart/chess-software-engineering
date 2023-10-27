from .figure import Figure
from ..errors import OutOfBoardError
from ..enums import Colors, Pieces

class Pawn(Figure):
    _symbol = 'P'
    kind: Pieces = Pieces.PAWN

    def updateMoves(self):
        result, moves = [], []
        if self.color == Colors.WHITE:
            if self.y == 2:
                moves += [(self.x, 3), (self.x, 4)]
            elif self.y < 8:
                moves.append((self.x, self.y + 1))
            cutMoves = (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)
        else:
            if self.y == 7:
                moves += [(self.x, 6), (self.x, 5)]
            elif self.y > 1:
                moves.append((self.x, self.y - 1))
            cutMoves = (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)

        for x, y in moves:
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                break
            if fig:
                break
            result.append((x, y))

        for x, y in cutMoves:
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                continue
            if fig and self.isEnemy(fig):
                result.append((x, y))
        self._moves = result