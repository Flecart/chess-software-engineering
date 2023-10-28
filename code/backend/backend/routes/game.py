from typing import Union
from backend.game.ChessGameManager import ChessGameManager
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
        if not __validate_move_format(move):
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
        return ChessGameManager().get_game(session_id).moves

        
    def __validate_move_format(move: str) -> bool:
        """ Just a quick way to check the move format, 
        TODO: should be moved to correct location later, if any
        
        Example correct format:
        e2e4
        """
        if len(move) != 4:
            return False
        
        letter_set = "abcdefgh"
        number_set = "12345678"

        if not move[0] in letter_set or not move[2] in letter_set:
            return False
        
        if not move[1] in number_set or not move[3] in number_set:
            return False
        
        return True
