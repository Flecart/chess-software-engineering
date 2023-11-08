from typing import Literal

from .errors import  NotFoundError, WrongFigureError, EndGame
from .board import Board
from .enums import Colors, Pieces
from .helpers import invert_color, pos2coors
from .figures import King
from .figures import Pawn

class Game:
    def __init__(self, 
                 figures: str | None = None, 
                 current_player: Colors = Colors.WHITE, 
                 cut: list[Pieces] = []):
        """ Creates a new game

        Args:
            figures (str | None, optional): If None, then a new game will be created. Defaults to None.
            current_player (Colors, optional): Current player. Defaults to Colors.WHITE.
            cut (list[Pieces], optional): List of cut figures (probably the pieces not present in the board, needs to check this). Defaults to [].
        """
        self.board: Board = Board(figures, cut)
        self.current_player: Colors = current_player

    def __str__(self):
        return self.board.__str__()

    @property
    def moves(self):
        return self.board.moves

    def compute_fen_color(self, color: Colors):
        return self.board.compute_obscure_fen(color,self.current_player)

    def compute_fen(self):
        return self.board.compute_fen(self.current_player)

    def get_color_board_view(self, color: Colors) -> str:
        return self.board.get_view(color)

    def get_board_view(self, last_player_view: bool = True) -> str:
        """Returns the board view after the last players move.
        """
        color = self.current_player
        if last_player_view:
            color = invert_color(color)

        return self.board.get_view(color)
    
    def has_moved(self, color: Literal["white"] | Literal["black"]) -> bool:
        """Returns True if the player with that color has moved, False otherwise
        """
        if color == "white":
            color = Colors.WHITE
        elif color == "black":
            color = Colors.BLACK
        else:
            raise ValueError("Invalid color")

        return color != self.current_player

    def get_color_board_view(self, color: Literal["white"] | Literal["black"]) -> str:
        """Returns the board view for the specified color
        """
        if color == "white":
            color = Colors.WHITE
        elif color == "black":
            color = Colors.BLACK
        else:
            raise ValueError("Invalid color")

        return self.board.get_view(color)

    def move(self, pos1: tuple[int, int], pos2: tuple[int, int]):
        figure = self.board.cell2Figure(*pos1)
        if not figure:
            raise NotFoundError
        if figure.color != self.current_player:
            raise WrongFigureError

        try:
            castled = isinstance(figure, King) and figure.try_to_castle(*pos2)
        except EndGame as exc:
            exc.figure = figure
            raise exc

        self.board.resetEnPassant()

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
    
    def get_moves(self):
        return self.board.moves
