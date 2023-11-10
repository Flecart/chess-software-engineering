from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from backend.game.interactive_player_manager import InteractivePlayerManager
from backend.game.players.manual_move_player import ManualMovePlayer


class ReturnUser(BaseModel):
    id: uuid.UUID

class GameState(BaseModel):
    your_turn: bool
    game_state: str

def create_user_routes(app:FastAPI,prefix:str=''):

    prefix = f"{prefix}/user"

    @app.get(prefix+"/new")
    def new_user():
        """
        A user is a player that can play a game.
        Is not a user in the application sense.
        So every client must create a new user
        before joining or creating a game.
        """
        player = ManualMovePlayer()
        InteractivePlayerManager().add_user(player)
        return ReturnUser(id=player.getId())

    @app.get(prefix+"/status/{user_id}")
    def your_turn(user_id:uuid.UUID):
        """
        Get the status of the game played by the user.
        Because the state of the game is different for every user.
        """
        user = InteractivePlayerManager().get_user(user_id)
        if user is None:
            return {
                "error": "user not found"
            }
        else:
            return GameState(your_turn=user.is_your_turn, game_state=user.last_game_state)

