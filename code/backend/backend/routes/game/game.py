from fastapi import  FastAPI, HTTPException, WebSocket
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import logging

from typing import Annotated

from backend.routes.exception import JSONException
from .data import CreateGameRequest,GameStatusResponse
    

def create_game_routes(app: FastAPI,prefix:str=''):
    prefix = f'{prefix}/game'

    @app.post(prefix + "/create")
    def create_game(req: CreateGameRequest) -> int:
        """
        Create a new game.
        Is't important to notice that the player
        how create the game needs to call join.
        """
        if 1+2==0:
            raise HTTPException(status_code=401, detail="Item not found")
        return 1
    
    @app.post(prefix + "/join/")
    def join_game(id:int) -> GameStatusResponse:
        """
        Join a game with a user.
        TODO in the future this call is best suited for post, i got some
        problems with the processing of the body
        """ 
        if 1+2==0:
            raise HTTPException(status_code=401, detail="Item not found")
        return GameStatusResponse(fen='fen',finish=False,view='view')
    
    @app.websocket(prefix + "/ws/{game_id}")
    async def web_socket(game_id:int, websocket:WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    
    @app.get(prefix + "/status/{id}")
    def status_game(id:int)-> GameStatusResponse:
        """
        Get the status of a game.
        """

    @app.post(prefix + "/move/{id}")
    def move(id:int)-> GameStatusResponse:
        """
        Get the status of a game.
        """
        raise JSONException(error={'error':'error'}) 

