from fastapi import  FastAPI,  WebSocket, Depends
from backend.game.v1_chess_game_manager import ChessGameManager
from typing import Annotated

from backend.routes.exception import JSONException
from backend.routes.auth import decode_access_token
from .data import CreateGameRequest,GameStatusResponse

from pydantic import BaseModel
from typing import Literal
import json
# TODO: move me to request nad responses file
class WebsocketRequests(BaseModel):
    kind: Literal["move", "join", "status"]
    data: str # TODO: da definire


def create_game_routes(app: FastAPI,prefix:str=''):
    prefix = f'{prefix}/game'

    @app.post(prefix)
    def create_game(req: CreateGameRequest) -> int:
        """
        Create a new game.
        Is't important to notice that the player
        how create the game needs to call join.
        """
        # TODO: log the request!
        return ChessGameManager().create_new_game(req)

    @app.websocket(prefix + "/{game_id}/ws")
    async def web_socket(game_id: int, websocket: WebSocket):
        """
        this web socket should be joined by a user to play

        Maybe this in a future could also be used to watch people play
        """
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            request = WebsocketRequests(**data)

            match request.kind:
                case "join":
                    # TODO: get correct request data for the socket join
                    ChessGameManager().join_socket(websocket, request.data)
                case "move":
                    # Mmmh, qui mancano le informazioni per fare la mossa
                    # forse potrebbe essere più sensato mettere il codice
                    # per i websocket in un socket manager che abbia anch'essa
                    # quelle informazioni.
                    # Una altra cosa è lasciare a quel manager la risposta
                    # quindi dovremmo spostare di nuovo il codice dei socket
                    # che ho messo a chess manager e chess game
                    ChessGameManager().move()
                case "status":
                    # rispondi con lo stato attuale a chi lo ha chiesto
                    pass
            await websocket.send_text(f"{data}")
    
    @app.put(prefix + "/{game_id}/join/")
    def join_game(game_id: int, token: Annotated[str, Depends(decode_access_token)]) -> GameStatusResponse:
        """
        Join a game with a user.
        TODO in the future this call is best suited for post, i(gio) got some
        problems with the processing of the body
        """ 
        print(token)
        return GameStatusResponse(fen='fen', finish=False, view='view')
    
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

