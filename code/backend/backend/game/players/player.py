from backend.engine.enums import Colors
import uuid
from abc import ABC, abstractmethod


class Player(ABC):
    """Implements an abstract player of the game.

    This class should be used to implement the different player types.
    As an example HumanPlayers or BotAIPlayers.
    
    """

    @abstractmethod
    def getId(self) -> uuid.UUID:
        pass

    @abstractmethod
    def join(self,game:uuid.UUID,game_state:str,current_player:Colors,color:Colors):
        pass

    @abstractmethod
    def update_move(self,game_state:str):
        pass
    
    @abstractmethod
    def game_end(self,reason:str):
        pass