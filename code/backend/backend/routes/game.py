from typing import Union
from backend.game.ChessGameManager import ChessGameManager
from backend.engine.helpers import validate_move_format
from fastapi import FastAPI
import uuid

def create_game_routes(app: FastAPI):
    prefix = '/game'

    @app.get(prefix + "/start")
    def start_game():
        return {
            "game-id": ChessGameManager().create_game()
        }

    @app.get(prefix + "/{session_id}/move/{move}")
    def move(session_id: uuid.UUID, move: str):
        if not validate_move_format(move):
            return {
                "error": "Invalid move format"
            }

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
            "board": game.get_board_view()
        }

    @app.get(prefix + "/{session_id}/moves")
    def get_moves(session_id: uuid.UUID):
        moves = ChessGameManager().get_game(session_id).moves
        end_result = []
        for move in moves:
            item  = dict(**move)
            item["figure"] = str(item["figure"])
            end_result.append(item)

        return end_result

        