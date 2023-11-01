from backend.engine.helpers import onBoard
from .figure import Figure
from ..errors import OutOfBoardError
from ..enums import Colors, Pieces

class Pawn(Figure):
    _symbol = 'P'
    kind: Pieces = Pieces.PAWN
    en_passant = False

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
        enPassantMoves = (self.x - 1, self.y), (self.x + 1, self.y)

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

        for x, y in enPassantMoves:
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                continue
            if fig and self.isEnemy(fig) and isinstance(fig, Pawn) and fig.en_passant:
                if self.color == Colors.WHITE:
                    result.append((x, y + 1))
                else:
                    result.append((x, y - 1))
        self._moves = result

    def allowEnPassant(self, x1: int, y1: int, x2: int, y2: int):
        if (self.color == Colors.WHITE and y1 == 2 and y2 == 4) or \
           (self.color == Colors.BLACK and y1 == 7 and y2 == 5):
            self.en_passant = True

    def getVisibleCells(self) -> list[tuple[int, int]]:
        all_moves = self.getMoves()

        if self.color == Colors.WHITE:
            front_moves = [(self.x - 1, self.y + 1), (self.x, self.y + 1), (self.x + 1, self.y + 1)]
        else:
            front_moves = [(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x + 1, self.y - 1)]
        front_moves = [(x, y) for x, y in front_moves if onBoard(x, y)]

        for position in front_moves:
            if position not in all_moves:
                all_moves.append(position)
        
        return all_moves

    def move(self, x, y):
        super(Pawn, self).move(x, y)
        if (self.color == Colors.WHITE and y == 8) or (self.color == Colors.BLACK and y == 1):
            self.board.transform(self)