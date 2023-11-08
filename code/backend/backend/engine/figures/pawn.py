from backend.engine.helpers import onBoard
from .figure import Figure
from ..errors import OutOfBoardError
from ..enums import Colors, Pieces

class Pawn(Figure):
    _symbol = 'P'
    kind: Pieces = Pieces.PAWN
    en_passant = False

    def updateMoves(self):
        result = []
        moves = []
        if self.color == Colors.WHITE:
            moves.append((self.x, self.y + 1))
            if self.y == 2:
                moves.append((self.x, self.y + 2))
            cut_moves = (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)
        else:
            moves.append((self.x, self.y - 1))
            if self.y == 7:
                moves.append((self.x, self.y - 2))
            cut_moves = (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)
        en_passant_squares = (self.x - 1, self.y), (self.x + 1, self.y)

        for x, y in moves:
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                break
            if fig is not None:
                break # this should work also with the first  move
            result.append((x, y))

        for x, y in cut_moves:
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                continue
            if fig is not None and self.isEnemy(fig):
                result.append((x, y))

        for x, y in en_passant_squares:
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                continue
            if fig is not None and self.isEnemy(fig) and isinstance(fig, Pawn) and fig.en_passant:
                if self.color == Colors.WHITE:
                    result.append((x, y + 1))
                else:
                    result.append((x, y - 1))

        self._moves = result
        print(str(self), self._moves)

    def getVisibleCells(self) -> list[tuple[int, int]]:
        all_moves = self.getMoves()

        if self.color == Colors.WHITE:
            front_moves = [(self.x - 1, self.y + 1), (self.x, self.y + 1), (self.x + 1, self.y + 1)]
        else:
            front_moves = [(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x + 1, self.y - 1)]
        front_moves = [(x, y) for x, y in front_moves if onBoard(x, y)]

        new_positions = [] # can't change all_moves
        for position in front_moves:
            if position not in all_moves:
                new_positions.append(position)
        
        return all_moves + new_positions

    def move(self, x: int, y: int):
        if self.color == Colors.WHITE and self.y == 2 and y == 4:
            self.en_passant = True
        elif self.color == Colors.BLACK and self.y == 7 and y == 5:
            self.en_passant = True

        super(Pawn, self).move(x, y)
        if (self.color == Colors.WHITE and y == 8) or (self.color == Colors.BLACK and y == 1):
            self.board.transform(self)
