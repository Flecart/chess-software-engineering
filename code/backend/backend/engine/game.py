from .errors import WrongTurnError, NotFoundError, WrongFigureError, EndGame
from .board import Board
from .enums import Colors, Pieces
from .helpers import invert_color, pos2coors
from .figures import King

class Game(object):
    def __init__(self, 
                 figures: Pieces | None = None, 
                 current_player: Colors = Colors.WHITE, 
                 cut: list[Pieces]=[]):
        """ Creates a new game

        Args:
            figures (Pieces | None, optional): If None, then a new game will be created. Defaults to None.
            current_player (Colors, optional): Current player. Defaults to Colors.WHITE.
            cut (list[Pieces], optional): List of cut figures (probably (TODO: check me) the pieces not present in the board). Defaults to [].
        """
        self.board = Board(figures, cut)
        self.current_player = current_player

    @property
    def moves(self):
        return self.board.moves

    def move(self, color, pos1: tuple[int, int], pos2: tuple[int, int]):
        if color != self.current_player:
            raise WrongTurnError
        figure = self.board.cell2Figure(*pos1)
        if not figure:
            raise NotFoundError
        if figure.color != color:
            raise WrongFigureError

        try:
            castled = isinstance(figure, King) and figure.try_to_castle(*pos2)
        except EndGame as exc:
            exc.figure = figure
            raise exc

        if not castled:
            result = figure, '{}-{}'.format(pos2coors(*pos1), pos2coors(*pos2))
            try:
                figure.move(*pos2)
            except EndGame as exc:
                exc.figure, exc.move = result
                raise exc
        else:
            result = figure, castled

        self.current_player = invert_color(self.current_player)
        return result
