from typing import Literal

from backend.engine.enums import Colors
from backend.game.players.player import Player
from ..engine import Game as DarkChessGame
from ..engine import helpers
from ..engine import errors

class ChessGame:
    """ The main class for a chess game. 

    By default creates a dark chess board.

    The difference between DarkChessGame and this class is 
    that this class is used to manage the game and the players,
    a notion that is not present in the DarkChessGame class.

    """
    
    def __init__(self):
        self.game = DarkChessGame()
        self.has_game_ended = False
        self.player = {
            Colors.WHITE: None,
            Colors.BLACK: None
        }

    @property
    def current_player(self) -> Colors:
        """Returns the current player"""
        return self.game.current_player

    @property
    def moves(self):
        """Returns the moves of the current game"""
        return self.game.moves

    def get_board_view(self, color: Colors) -> str:
        """Returns the current board view"""
        return self.game.get_color_board_view(color)

    def get_color_board_view(self, color: Literal["white"] | Literal["black"]) -> str:
        """Returns the current board view for the specified color"""
        return self.game.get_color_board_view(color)
    
    def has_moved(self, color: Literal["white"] | Literal["black"]) -> bool:
        """Returns True if the player with that color has moved, False otherwise"""
        return self.game.has_moved(color)

    def has_ended(self) -> bool:
        """Returns True if the game has ended, False otherwise"""
        return self.has_game_ended

    def get_color_from_player(self,player:Player) -> Colors|None:

        for color in [Colors.BLACK,Colors.WHITE]:
            if player.getId() == self.player[color].getId():
                return color
        return None

    def join(self,player:Player,color:Colors|None):
        if color is None:
           color = Colors.WHITE if self.player[Colors.WHITE] is None else Colors.BLACK
        if self.player[color] is not None:
            raise Exception("Color already taken")
        self.player[color] = player
        return color


    def add_move(self,player:Player, move: str) -> bool:
        """Adds a move to the current game
        
        Returns:
            bool: True if the move was added, False otherwise
        """
        # TODO: transform the PGN move string into dark chess format
        # currently is just algebraic notation

        color =  self.get_color_from_player(player)

        if color is None:
            raise Exception("Player not in game")

        start_position = helpers.coors2pos(move[:2])
        end_position = helpers.coors2pos(move[2:])


        if color != self.game.current_player:
            raise errors.WrongTurnError()
        try: 
            self.game.move(start_position, end_position)
            #TODO(gio):gestire la fine della partita
            next = self.game.current_player
            self.player[next].update_move(self.get_board_view(next))
        except errors.EndGame:
            # TODO: test what happens when you move even if the game has ended
            self.has_game_ended = True
        
        return True

    def invert_colors(color: Literal["white"] | Literal["black"]) -> Literal["white"] | Literal["black"]:
        """Inverts the color"""
        if color == "white":
            return "black"
        elif color == "black":
            return "white"
        else:
            raise ValueError("Invalid color")
