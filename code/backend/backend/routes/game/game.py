from logging import Logger
from fastapi import  FastAPI,  WebSocket, Depends
from fastapi.encoders import jsonable_encoder
from backend.game.utils import Color
from backend.game.v1_chess_game_manager import ChessGameManager
from typing import Annotated
from backend.game.v1_socket_manager import SocketManager

from backend.routes.exception import JSONException
from backend.routes.auth import decode_access_token
from .data import CreateGameRequest,GameStatusResponse

from pydantic import BaseModel
from typing import Literal
import asyncio
import json

# TODO: move me to request nad responses file
class WebsocketRequests(BaseModel):
    kind: Literal["move", "list_move", "status"]
    data: str # ha senso solamente per la move, e definisce la mossa e.g. e2e4


def create_game_routes(app: FastAPI,prefix:str=''):
    prefix = f'{prefix}/game'

    @app.post(prefix)
    def create_game(req: CreateGameRequest, user_data: Annotated[dict, Depends(decode_access_token)]) -> int:
        """
        Create a new game.
        Is't important to notice that the player
        how create the game needs to call join.
        """
        # TODO: log the request!
        return ChessGameManager().create_new_game(req)

    @app.websocket(prefix + "/{game_id}/{token}/ws")
    async def web_socket(game_id: int,token:str, websocket: WebSocket):
        """
        this web socket should be joined by a user to play

        Maybe this in a future could also be used to watch people play
        """
        user_data = decode_access_token(token)
        username = user_data["username"]
        await websocket.accept()

        game = ChessGameManager().get_game(game_id)
        player_color = game.get_player_color(username)
        await SocketManager().join(game_id, username, websocket)

        while True:
            if SocketManager().is_socket_reading(game_id, websocket):
                # TODO: refactor me, and put me in socket manager?
                data = await websocket.receive_json()
                request = WebsocketRequests(**data)
                list_moves = None
                move = None
                match request.kind:
                    case "move":
                        # manda lo stato aggiornato a tutti i giocatori

                        # Mmmh, qui mancano le informazioni per fare la mossa
                        # forse potrebbe essere più sensato mettere il codice
                        # per i websocket in un socket manager che abbia anch'essa
                        # quelle informazioni.
                        # Una altra cosa è lasciare a quel manager la risposta
                        # quindi dovremmo spostare di nuovo il codice dei socket
                        # che ho messo a chess manager e chess game
                        try:
                            game.move(request.data)
                            await SocketManager().notify_opponent(game_id, player_color) 
                            move = request.data
                        except Exception as e:
                            pass
                    case "status":
                        # rispondi con lo stato attuale a chi lo ha chiesto, con solamente una fen
                        # TODO: nello status bisogna mettere anche il nome dei giocatori.
                        if not (player_color == Color.WHITE and player_color == Color.BLACK):
                            raise Exception("Watching player not supported yet")
                    case "list_move":
                        # rispondi con la lista delle mosse 

                        # trova colore fai check colore player corrente 
                        if player_color == game.current_player:
                            list_moves = game.get_moves()

                data = game.get_player_response(player_color\
                            ,possible_moves=list_moves,move_made=move)
                await websocket.send_json(jsonable_encoder(data))
            else:
                await websocket.send_json({"waiting": True})
                await asyncio.sleep(1) 
    
    @app.put(prefix + "/{game_id}/join/")
    def join_game(game_id: int, user_data: Annotated[dict, Depends(decode_access_token)]):
        """
        Join a game with a user.
        TODO in the future this call is best suited for post, i(gio) got some
        problems with the processing of the body

        token:
            dict of username string, and guest boolean
        """ 
        is_white = True
        try:
            try:
                ChessGameManager().get_game(game_id).join(user_data['username'], Color.WHITE)
            except:
                ChessGameManager().get_game(game_id).join(user_data['username'], Color.BLACK)
                is_white = False
        except ValueError as e:
            raise JSONException(error={'error': str(e)}, status_code=400)
        
        return {"data": f"user has correctly joined game {game_id} as {'white' if is_white else 'black'}"}

    
    @app.get(prefix + "/{game_id}")
    def status_game(game_id: int)-> GameStatusResponse:
        """
        Get the status of a game.
        """
        pass

    @app.post(prefix + "{game_id}/move")
    def move(game_id:int)-> GameStatusResponse:
        """
        Get the status of a game.
        """
        raise JSONException(error={'error':'error'}) 

