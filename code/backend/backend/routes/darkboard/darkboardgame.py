from fastapi import  FastAPI
from backend.bot.darkboard_adapter import DarkBoardSingleton, DarkBoardStates
from backend.routes.darkboard.data import GameStatusResponse
from backend.routes.exception import JSONException

GameOverMessage=  'Game is over, go back in the main page and create a new game'

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
        if DarkBoardSingleton().get_state == DarkBoardStates.GAME_OVER:
            raise JSONException(status_code=400, error=GameOverMessage)
        if DarkBoardSingleton().get_state == DarkBoardStates.ERROR:
            raise JSONException(status_code=400, error=DarkBoardSingleton().get_error_message)

    @app.post(prefix + "/move")
    def move():
        """
        Make a move.
        """
        check_valid_status()
        try:
            import threading
            thread = threading.Thread(target=DarkBoardSingleton().make_best_move)
            thread.start()
        except Exception as e:
            print(e)
            raise JSONException(status_code=400, error=str(e))
        return  "ok"


    @app.get(prefix + "/status")
    def get_status():
        """
        Get the status of a game.
        """

        check_valid_status()
        try:
            state = DarkBoardSingleton().get_state
            # needs to know if he can make the move, an also in a future the message, 
            # we can create a new ds
            
            fen = DarkBoardSingleton().get_fen

            return GameStatusResponse(fen=fen, state=state, message=DarkBoardSingleton().get_message)
        except Exception as e:
            print(e)
            raise JSONException(status_code=400, error=GameOverMessage)
