"""
Game manager for the new version of api games
"""
from fastapi import WebSocket

from backend.routes.game.data import CreateGameRequest
from backend.game.v1_chess_game import ChessGame
from backend.game.utils import Color
from backend.routes.auth import decode_access_token

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
        self.__games: dict[int, ChessGame] = {}
        self.__white_games: dict[int, int] = {}
        self.__black_games: dict[int, int] = {}

        # this should be deleted when connected to db
        self.__games_n = 0
    
    # TODO in a future should also check the permission of the user
    def get_game(self, id: int) -> ChessGame:
        return self.__games[id]

    def create_new_game(self, game_creation: CreateGameRequest) -> int:
        self.__games_n += 1
        self.__games[self.__games_n] = ChessGame(game_creation)
        return self.__games_n

    def join(self, game_id: int, player: int, color: Color) -> None:
        if color == Color.WHITE:
            if self.__white_games.get(player) is not None:
                raise ValueError("white player already joined")
            self.__white_games[player] = game_id
        elif color == Color.BLACK:
            if self.__black_games.get(player) is not None:
                raise ValueError("black player already joined")
            self.__black_games[player] = game_id
        else:
            raise ValueError("color must be white or black")

    def move(self, game_id: int, player: int, move: str) -> None:
        game = self.__games[game_id]
        if game.current_player == Color.WHITE:
            if self.__white_games.get(player) is None:
                raise ValueError("white player has not joined")
        elif game.current_player == Color.BLACK:
            if self.__black_games.get(player) is None:
                raise ValueError("black player has not joined")
        else:
            raise ValueError("color must be white or black")

        game.move(move)

    def get_view(self, game_id: int, color: Color) -> str:
        # NOTE: is it better to keep the property a string, or better
        # to encapsulate?
        game = self.__games[game_id]
        if color == Color.WHITE:
            return game.white_view
        elif color == Color.BLACK:
            return game.black_view
        else:
            raise ValueError("color must be white or black")

    def get_moves(self, game_id: int) -> list[str]:
        return self.__games[game_id].get_moves()