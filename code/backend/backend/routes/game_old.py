from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uuid

from backend.game.chess_game_manager import ChessGameManager
from backend.game.chess_game import ChessGame
from backend.engine.helpers import validate_move_format

def create_game_routes(app: FastAPI):
    prefix = '/game'

    @app.get(prefix + "/start")
    def start_game():
        return {
            "game-id": ChessGameManager().create_game()
        }

    @app.get(prefix + "/{game_id}/board/{player}")
    def get_board(game_id: uuid.UUID, player: str):
        # TODO: we should refactor these endpoints so that we have a form of authentication

        if player != "white" and player != "black":
            return JSONResponse({
                "error": "Invalid player"
            }, status_code=400)

        game = ChessGameManager().get_game(game_id)
        if game is None:
            return JSONResponse({
                "error": "Game not found"
            }, status_code=404)

        return {
            "has_enemy_moved": game.has_moved(ChessGame.invert_colors(player)),
            "board": game.get_color_board_view(player)
        }

    @app.get(prefix + "/{game_id}/move/{move}", status_code=200) # TODO: move me to POST
    def move(game_id: uuid.UUID, move: str):
        if not validate_move_format(move):
            return JSONResponse({
                "error": "Invalid move format"
            }, status_code=400)

        game = ChessGameManager().get_game(game_id)
        if game is None:
            return JSONResponse({
                "error": "Game not found"
            }, status_code=404)
        
        move_successful = game.add_move(move)
        if not move_successful:
            return JSONResponse({
                "error": "Invalid move"
            }, status_code=400)
        
        if game.has_ended():
            return {
                "game_ended": True
            }
        
        # return the board representation
        return {
            "game_ended": False,
            "board": game.get_board_view()
        }

    @app.get(prefix + "/{game_id}/moves", status_code=200)
    def get_moves(game_id: uuid.UUID):
        moves = ChessGameManager().get_game(game_id).moves
        end_result = []
        for move in moves:
            item  = dict(**move)
            item["figure"] = str(item["figure"])
            end_result.append(item)

        return end_result
