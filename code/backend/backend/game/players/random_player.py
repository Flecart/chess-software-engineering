
from backend.engine.enums import Colors
from backend.game.chess_game_manager import ChessGameManager
from .player import Player
import uuid

class RandomPlayer(Player):

    def __init__(self):
        self._uuid = uuid.uuid4()
        self._move_n=0

    def getId(self) -> uuid.UUID:
        return self._uuid
        
    def join(self,game:uuid.UUID,game_state:str,current_player:Colors,color:Colors):
        self._game = game
        if color == Colors.WHITE:
            raise Exception("RandomPlayer can only be black")


    def update_move(self,game_state:str):
        if self._move_n == 0:
            self._next_move = "d7d6"
        else:
            self._next_move = "c8d7"
            if self._move_n%2 == 0:
                self._next_move = 'd7c8'#  self._next_move
        self._move_n+=1
        
        ChessGameManager().get_game(self._game).add_move(self,self._next_move)
    
    def game_end(self,reason:str):
        pass
    
    
