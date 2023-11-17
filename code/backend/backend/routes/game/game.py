from fastapi import  FastAPI,  WebSocket, Depends
from backend.game.utils import Color
from backend.game.v1_chess_game_manager import ChessGameManager
from typing import Annotated
from backend.game.v1_socket_manager import SocketManager

from backend.routes.exception import JSONException
from backend.routes.auth import decode_access_token
from .data import CreateGameRequest,GameStatusResponse

from pydantic import BaseModel
from typing import Literal
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

    @app.websocket(prefix + "/{game_id}/ws")
    async def web_socket(game_id: int, websocket: WebSocket, user_data: Annotated[dict, Depends(decode_access_token)]):
        """
        this web socket should be joined by a user to play

        Maybe this in a future could also be used to watch people play
        """
        """"
        TO Test
        const serverUrl = 'ws://localhost:8000/game/1/ws';
        const authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJndWVzdCI6ZmFsc2UsImV4cCI6MTcwMDI0MzM0MX0.eQgGYZeu2CEvgYjUdhOiWF_hmaU8B4MXbfh_TO5zxls';

        // Create a WebSocket connection with the authentication header
        const socket = new WebSocket(serverUrl, ['Authorization', authToken]);
        socket.addEventListener('open', (event) => {
            console.log('WebSocket connection opened:', event);
        });
        socket.addEventListener('message', (event) => {
            console.log('Message from server:', event.data);
        });
        socket.addEventListener('error', (event) => {
            console.error('WebSocket error:', event);
        });
        socket.addEventListener('close', (event) => {
            console.log('WebSocket connection closed:', event);
        });

        """
        await websocket.accept()

        username = user_data["username"]
        game = ChessGameManager().get_game(game_id)
        player_color = game.get_player_color(username)
        SocketManager().join(game_id, username, websocket)

        while True:
            data = await websocket.receive_json()
            request = WebsocketRequests(**data)

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
                        game.move(player_color, request.data)
                        #SocketManager().broadcast(game_id, ) 
                        data = True
                    except:
                        data = False
                case "status":
                    # rispondi con lo stato attuale a chi lo ha chiesto, con solamente una fen
                    if player_color == Color.WHITE:
                        data = game.white_view
                    elif player_color == Color.BLACK:
                        data = game.black_view
                    else:
                        raise Exception("Watching player not supported yet")
                case "list_move":
                    # rispondi con la lista delle mosse 

                    # trova colore fai check colore player corrente 
                    if player_color == game.current_player:
                        data = game.list_moves()
                    else:
                        data = []
                    
            await websocket.send_json(data)
    
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

