from fastapi import  FastAPI
from backend.bot.darkboard_adapter import DarkBoardSingleton, DarkBoardStates
from backend.routes.darkboard.data import GameStatusResponse
from backend.routes.exception import JSONException

def create_game_routes(app: FastAPI,prefix:str=''):
    prefix = f'{prefix}/darkboard'

    @app.post(prefix + "/start")
    def create_game():
        """
        Creates a new game.
        """
        DarkBoardSingleton().create_game()
        return  "ok"
    
    def check_valid_status():
        state = DarkBoardSingleton().get_state
        if state == DarkBoardStates.GAME_OVER:
            raise JSONException(status_code=400, error="Game is over")

    @app.post(prefix + "/move")
    def move():
        """
        Make a move.
        """
        try:
            check_valid_status()
            import threading
            thread = threading.Thread(target=DarkBoardSingleton().make_best_move)
            thread.start()
        except Exception as e:
            print(e)
            raise JSONException(status_code=400, error="Game is over",)
        return  "ok"


    @app.get(prefix + "/status")
    def get_status():
        """
        Get the status of a game.
        """

        # TODO: refactor me
        try:
            state = DarkBoardSingleton().get_state
            # needs to know if he can make the move, an also in a future the message, 
            # we can create a new ds
            
            if state == DarkBoardStates.GAME_OVER:
                return GameStatusResponse(fen=None, state=DarkBoardSingleton().get_state,message=None)
            
            fen = DarkBoardSingleton().get_fen

            return GameStatusResponse(fen=fen, state=state, message=None)
        except Exception as e:
            print(e)
            raise JSONException(status_code=400, error="Game has not started yet")
