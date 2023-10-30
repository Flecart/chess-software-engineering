from backend.engine.enums import Colors
from .player import Player
import uuid

class ManualMovePlayer(Player):

    def __init__(self):
        self._id = uuid.uuid4()
        self._last_game_state = None
        
    @property
    def last_game_state(self):
        return self._last_game_state

    @property
    def is_your_turn(self) -> bool:
        return self._is_your_turn

    def getId(self) -> uuid.UUID:
        return self._id
        
    def join(self,game: uuid.UUID, game_state: str, current_player: Colors, color: Colors):
        self._last_game_state = game_state
        self._game = game
        self._is_your_turn = current_player == color
        self._color = color

    #TODO: per ora non è random e funziona solo con il nero
    def update_move(self, game_state: str):
        self._last_game_state = game_state
        self._is_your_turn = True

    
    def game_end(self, reason: str):
        """ Tell the player that the game has ended.
        """
        pass
    
    
