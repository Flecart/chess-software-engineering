from typing import Union
from backend.game.ChessGameManager import ChessGameManager
from fastapi import FastAPI
import uuid

def create_game_routes(app: FastAPI):
    prefix = '/game'

    @app.get(prefix + "/start")
    def start_game() -> uuid.UUID:
        return ChessGameManager().create_game()

    @app.get(prefix + "{session_id}/move/{move}")
    def move(session_id: uuid.UUID, move: str) -> :
        game = ChessGameManager().get_game(session_id)
        if game is None:
            return {
                "error": "game not found"
            }
        
        move_successful = game.add_move(move)
        if not move_successful:
            return {
                "error": "Invalid move"
            }
        
        if game.has_ended():
            return {
                "game_ended": True
            }
        
        # return the board representation
        return {
            "game_ended": False,
            "board": game.game.board
        }
            return 'ok'

    @app.get(prefix + "/{sessions_id}/moves")
    def get_moves(sessoion_id: uuid.UUID):
        return ChessGameManager().get_game(sessoion_id).moves

        
