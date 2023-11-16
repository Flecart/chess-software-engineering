from fastapi import  FastAPI,  WebSocket
from 

from backend.routes.exception import JSONException
from .data import CreateGameRequest,GameStatusResponse
    

def create_game_routes(app: FastAPI,prefix:str=''):
    prefix = f'{prefix}/game'

    @app.post(prefix)
    def create_game(req: CreateGameRequest) -> int:
        """
        Create a new game.
        Is't important to notice that the player
        how create the game needs to call join.
        """


        return 42


    @app.websocket(prefix + "/{game_id}/ws")
    async def web_socket(game_id: int, websocket:WebSocket):
        """
        this web socket should be joined by a user ho play

        Maybe this in a future could also be used to watch people play
        """
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{data}")
    
    @app.put(prefix + "/{game_id}/join/")
    def join_game(game_id:int,) -> GameStatusResponse:
        """
        Join a game with a user.
        TODO in the future this call is best suited for post, i got some
        problems with the processing of the body
        """ 
        return GameStatusResponse(fen='fen',finish=False,view='view')
    
    
    @app.get(prefix + "/{game_id}")
    def status_game(game_id:int)-> GameStatusResponse:
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

