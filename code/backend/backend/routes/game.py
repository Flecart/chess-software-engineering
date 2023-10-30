from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import logging

from backend.engine.enums import Colors
from backend.game.chess_game_manager import ChessGameManager
from backend.engine.helpers import validate_move_format
from backend.game.interactive_player_manager import InteractivePlayerManager
from backend.game.players.random_player import RandomPlayer

class JoinGame(BaseModel):
    game_id: uuid.UUID
    player_id: uuid.UUID
    color: str

def create_game_routes(app: FastAPI, prefix: str=''):
    prefix = f'{prefix}/game'

    @app.get(prefix + "/create")
    def create_game():
        """
        Create a new game.
        Is't important to notice that the player
        how create the game needs to call join.
        """
        logging.info("Creating game")
        return {
            "game_id": ChessGameManager().create_game()
        }
    
    @app.get(prefix + "/join/{game_id}/{player_id}/{color}")
    def join_game(game_id: uuid.UUID, player_id: uuid.UUID, color: str):
        """
        Join a game with a user.
        TODO in the future this call is best suited for post, i got some
        problems with the processing of the body
        """ 
        data = JoinGame(game_id=game_id,player_id=player_id,color=color)
        player = InteractivePlayerManager().get_user(data.player_id)
        if  player is None:
            return {
                "error": "user not found"
            }
        else:
            color = Colors.WHITE if data.color == "white" else Colors.BLACK
            ChessGameManager().set_player(data.game_id,player,color)
            return {
                "game-id": data.game_id
            }

    @app.get(prefix + "/add-bot/{game}/")
    def addBot(game:uuid.UUID):
        """
        Add a bot to the game.
        TODO: in the current implementation the bot is always black
        """
        if game is None:
            return {
                "error": "game not found"
            }
        
        bot = RandomPlayer()
        ChessGameManager().set_player(game,bot,Colors.BLACK)

    @app.get(prefix + "/move/{session_id}/{user}/{move}")
    def move(session_id: uuid.UUID, user: uuid.UUID,move: str):
        """
        Move a pice in the game.
        The move format is for example "a2a3"
        so the first two characters are the starting position
        and the last two are the ending position.
        """
        player = InteractivePlayerManager().get_user(user)
        if player is None:
            return {
                "error": "user not found"
            }

        if not validate_move_format(move):
            return {
                "error": "Invalid move format"
            }

        if player != "white" and player != "black":
            return JSONResponse({
                "error": "Invalid player"
            }, status_code=400)

        game = ChessGameManager().get_game(session_id)
        if game is None:
            return {
                "error": "game not found"
            }

        move_successful = game.add_move(player, move)

        if not move_successful:
            return JSONResponse({
                "error": "Invalid move"
            }, status_code=400)
        
        if game.has_ended():
            return {
                "game_ended": True
            }
        
        return {
            "game_ended": False,
            "board": game.get_board_view(player._color)
        }

