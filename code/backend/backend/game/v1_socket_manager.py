
from fastapi import WebSocket
import websockets
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
        self.__web_sockets: dict[int, list[tuple[str, WebSocket]]] = {}

    def join(self,game_id: int,username: str, websocket: WebSocket):
        game = ChessGameManager().get_game(game_id) 
        if game_id not in self.__web_sockets:
            self.__web_sockets[game_id] = []
        
        self.__web_sockets[game_id].append((username, websocket))


    async def broadcast(self, game_id: int, current_player_color: Color) -> None:
        """
        Sends the current state to both players
        """
        game = ChessGameManager().get_game(game_id)
        sockets = []
        for connections in self.__web_sockets[game_id]:
            # we also should remove time out socket and close them
            # and make this thing async
            ## TODO da refactorare 
            player_color = game.get_player_color(connections[0])
            if player_color != current_player_color:
                sockets.append(connections[1])
        
        websockets.broadast(sockets,GameResponse(kind="status",data=game.get_player_response(current_player_color)))




