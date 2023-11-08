from abc import ABC, abstractmethod

from ..enums import Colors, Pieces
from .. import errors
from ..helpers import pos2coors

class Figure:
    color: Colors | None = None
    kind: Pieces = None
    _symbol: str = '?'

    def __init__(self, x: int, y: int, color: Colors, board):
        from ..board import Board # just for type hinting, needs to be here for circular imports.
        
        self.x: int = x
        self.y: int = y
        self.color: Colors = color
        self.board: Board = board
        self._moves: None | list[tuple[int, int]] = None
        self._moved: bool = False

    def __str__(self):
        return '{}{}'.format(self.symbol, pos2coors(self.x, self.y))
    
    @property
    def symbol(self):
        if self.color == Colors.WHITE:
            return self._symbol.upper()
        return self._symbol.lower()

    @property
    def moved(self):
        return self._moved

    def getMoves(self):
        print("get moves called", str(self), self._moves)
        if self._moves is None:
            self.updateMoves()
            print("updated moves", self._moves)
        return self._moves

    @abstractmethod
    def updateMoves(self):
        """ Updates the current possible moves of the figure
        """
        raise NotImplementedError

    def move(self, x: int, y: int):
        print("move", str(self), self.getMoves())
        if (x, y) not in self.getMoves():
            raise errors.WrongMoveError
        self.board.move(self, x, y)
        self._moved = True

    def isEnemy(self, figure):
        return figure.color != self.color

    def isFriend(self, figure):
        return figure.color == self.color

    def getLineMoves(self, deltaList):
        # TODO-3(gio/angi) codice non perfetto chi vuole può refactorarlo
        moves = []
        for dx, dy in deltaList:
            if dx == 0 and dy == 0:
                continue
            x, y = self.x, self.y
            while True:
                x += dx
                y += dy
                try:
                    fig = self.board.cell2Figure(x, y)
                except errors.OutOfBoardError:
                    break
                if fig:
                    if self.isEnemy(fig):
                        moves.append((x, y))
                    break
                moves.append((x, y))
        return moves

    def update(self):
        self.updateMoves()

    def reset(self):
        _moves = None

    def terminate(self):
        """ Eliminates the selected piece from the board
        """

        self.board._figures[self.color][self.kind].remove(self)

    def getVisibleCells(self):
        return self.getMoves()
