
import asyncio
from fastapi import WebSocket
from fastapi.websockets import WebSocketState

from .utils import Color
from fastapi.encoders import jsonable_encoder

from backend.game.v1_chess_game_manager import ChessGameManager



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

    
    async def join(self, game_id: int, username: str, websocket: WebSocket):
        """
        Should send the current state of the game, and make only one socket in
        waiting for receing data (is on)
        
        """
        game = ChessGameManager().get_game(game_id) 
        if game_id not in self.__web_sockets:
            self.__web_sockets[game_id] = []
        self.__web_sockets[game_id].append((username, websocket))
        player_color = game.get_player_color(username)
        data = game.get_player_response(player_color)
        await websocket.send_json(jsonable_encoder(data))
        

    def is_socket_reading(self, game_id: int, websocket: WebSocket) -> bool:
        """ Returns a boolean that says if the current websocket shouldd listen or should write
        """
        game = ChessGameManager().get_game(game_id)
        players_sockets = self.__web_sockets[game_id]
        
        for player, socket in players_sockets:
            if game.is_current_player(player) and socket == websocket:
                return True

        game.get_bot_move(asyncio.get_running_loop())
        return False

    async def notify_opponent(self, game_id: int, current_player_color: Color) -> None:
        """
        """
        game = ChessGameManager().get_game(game_id)
        to_remove = []
        for (name, ws) in self.__web_sockets[game_id]:
            # we also should remove time out socket and close them
            # and make this thing async
            ## TODO da refactorare 
            player_color = game.get_player_color(name)
            # check ws connection is open
            if ws.client_state == WebSocketState.DISCONNECTED:
                to_remove.append((name, ws))
                continue
            if player_color is not None and player_color != current_player_color:
                ren = game.get_player_response(player_color)
                await ws.send_json(jsonable_encoder(ren))


        for (name, ws) in to_remove:
            await self.remove(game_id, name, ws)
        
    async def remove(self, game_id: int, username: str, websocket: WebSocket):
        """
        """
        self.__web_sockets[game_id].remove((username, websocket))
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()




