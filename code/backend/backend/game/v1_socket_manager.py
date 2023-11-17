
from fastapi import WebSocket
from .utils import Color

from backend.game.v1_chess_game_manager import ChessGameManager
from backend.routes.game.data import GameStatusResponse

from pydantic import BaseModel
from typing import Literal

# TODO: refactor, move me to response and answer format folder
class GameResponse(BaseModel):
    kind: Literal["status"] # add with other types
    data: GameStatusResponse


class SocketManager:
    """
    This class is a singleton that manages all the sockets
    and associated with game_id.

    It is used to comunicate in real time.
    """
    _instance: "SocketManager" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init()
        return cls._instance
    
    def __init(self):
        # chiave id_partita, linka, utente - websocket
        self.__web_sockets: dict[int, list[(str, WebSocket)]] = {}

    def join(self,game_id: int,username: str, websocket: WebSocket):
        game = ChessGameManager().get_game(game_id) 
        if game_id not in self.__web_sockets:
            self.__web_sockets[game_id] = []
        
        self.__web_sockets[game_id].append((username, websocket))


    def broadcast(self, game_id: int, data: str) -> None:
        """
        Sends the current state to both players
        """
        for dict in self.__web_sockets[game_id]:
            # we also should remove time out socket and close them
            # and make this thing async
            dict["websocket"].send_text(data)




