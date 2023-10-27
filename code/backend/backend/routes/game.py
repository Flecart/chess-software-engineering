from typing import Union
from backend.game.ChessGameManager import ChessGameManager
from fastapi import FastAPI
import uuid

def create_game_routes(app: FastAPI):
    prefix = '/game'

    @app.get(prefix + "/start")
    def start_game():
        return ChessGameManager().create_game()

    @app.get(prefix + "{session_id}/move/{move}")
    def move(session_id: uuid.UUID, move: str):
        game = ChessGameManager().get_game(session_id)
        if game is None:
            return None
        else: 
            game.add_move(move)
            return 'ok'

    @app.get(prefix + "/{sessions_id}/moves")
    def get_moves(sessoion_id: uuid.UUID):
        return ChessGameManager().get_game(sessoion_id).moves

        
