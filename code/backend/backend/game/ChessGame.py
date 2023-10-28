from ..engine import Game as DarkChessGame
from ..engine import helpers
from ..engine import errors

class ChessGame:
    """ The main class for a chess game. 

    By default creates a dark chess board.
    
    """
    def __init__(self):
        self.game = DarkChessGame()
        self.has_game_ended = False

    @property
    def moves(self):
        """Returns the moves of the current game"""
        return self.game.moves

    def get_board_view(self) -> str:
        """Returns the current board view"""
        return self.game.get_board_view()

    def has_ended(self) -> bool:
        """Returns True if the game has ended, False otherwise"""
        return self.has_game_ended

    def add_move(self, move: str) -> bool:
        """Adds a move to the current game
        
        Returns:
            bool: True if the move was added, False otherwise
        """
        # TODO: transform the PGN move string into dark chess format
        # currently is just algebraic notation

        start_position = helpers.coors2pos(move[:2])
        end_position = helpers.coors2pos(move[2:])

        try: 
            self.game.move(start_position, end_position)
        except (errors.NotFoundError, errors.WrongFigureError, errors.WrongMoveError):
            return False
        except errors.EndGame:
            # TODO: test what happens when you move even if the game has ended
            self.has_game_ended = True
        
        return True
