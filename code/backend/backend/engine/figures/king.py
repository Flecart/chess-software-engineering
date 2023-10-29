from .figure import Figure
from ..enums import Pieces, Colors
from ..errors import OutOfBoardError, WrongMoveError, EndGame,NotFoundError
from ..helpers import onBoard

class King(Figure):
    _symbol = 'K'
    kind = Pieces.KING

    def updateMoves(self):
        from ..const import KING_MOVES
        moves = []
        for dx, dy in KING_MOVES:
            x = self.x + dx
            y = self.y + dy
            try:
                fig = self.board.cell2Figure(x, y)
            except OutOfBoardError:
                continue
            if not fig or self.isEnemy(fig):
                moves.append((x, y))
        if self.can_castle(True):
            moves.append((self.x + 2, self.y))
        if self.can_castle(False):
            moves.append((self.x - 2, self.y))
        self._moves = moves

    def updateAura(self):
        from ..const import KING_MOVES
        # deprecated because king can be cut
        aura = []
        for dx, dy in KING_MOVES:
            x = self.x + dx
            y = self.y + dy
            if onBoard(x, y):
                aura.append((x, y))
        self._aura = aura

    def royalAura(self):
        # deprecated because king can be cut
        if self._aura is None:
            self.updateAura()
        return self._aura

    def reset(self):
        super(King, self).reset()
        self._aura = None

    def can_castle(self, short: bool = True):
        if self.moved:
            return False

        if self.color == Colors.WHITE:
            y = 1
        else:
            y = 8

        if short:
            rook_x: int = 8
            cells = ((6, y), (7, y))
        else:
            rook_x: int = 1
            cells = ((2, y), (3, y), (4, y))

        try:
            rook = self.board.cell2Figure(x=rook_x, y=y)
        except (NotFoundError, OutOfBoardError):
            return False

        if not rook or rook.moved:
            return False

        for cell in cells:
            try:
                if self.board.cell2Figure(*cell):
                    return False
            except OutOfBoardError:
                return False

        return rook

    def castle(self, short: bool = True):
        rook = self.can_castle(short)
        if not rook:
            raise WrongMoveError
        self.board.castle(self, rook)

    def try_to_castle(self, x: int, y: int):
        if (self.color == Colors.WHITE and (x, y) in ((7, 1), (3, 1))) or \
           (self.color == Colors.BLACK and (x, y) in ((7, 8), (3, 8))):
            try:
                self.castle(x == 7)
                move = '0-0' if x == 7 else '0-0-0'
            except WrongMoveError:
                pass
            except EndGame as e:
                e.move = move
                raise e
            else:
                return move

        return False

    def remove(self, *args, **kwargs):
        del self

    def getVisibleCells(self):
        return self.getMoves()