# create singleton
import uuid

from backend.game.ChessGame import ChessGame

class ChessGameManager:
    _instance: "ChessGameManager" | None = None
    games: dict[uuid.UUID, ChessGame]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init()
        return cls._instance
    
    def __init(self):
        self.games = {}

    def get_game(self, game_id:uuid) -> ChessGame | None:
        return self.games.get(game_id, None)

    def create_game(self) -> uuid.UUID:
        game_id = uuid.uuid4()
        while (game_id in self.games):
            game_id = uuid.uuid4()

        self.games[game_id] = ChessGame()
        return game_id

