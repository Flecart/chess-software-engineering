# create singleton
import uuid
from backend.engine.enums import Colors

from backend.game.chess_game import ChessGame
from backend.game.players.player import Player

class ChessGameManager:
    """
    This class is a singleton that manages all the games
    and associated id.

    It is used to create a new game and to get a game
    from its id.
    """
    _instance: "ChessGameManager" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init()
        return cls._instance
    
    def __init(self):
        self.games = {}

    def get_game(self, game_id: uuid.UUID) -> ChessGame | None:
        return self.games.get(game_id, None)

    def set_player(self,game: uuid.UUID, player: Player, color = Colors|None) -> uuid.UUID:
        gameInstance = self.get_game(game)
        if gameInstance is None:
            raise ValueError("game not found")
        color = gameInstance.join(player, color)
        player.join(game,gameInstance.get_board_view_fen(color),gameInstance.current_player,color)
 

    def create_game(self) -> uuid.UUID:
        game_id = uuid.uuid4()
        while (game_id in self.games):
            game_id = uuid.uuid4()
        game = ChessGame()
        self.games[game_id] = game
        return game_id

