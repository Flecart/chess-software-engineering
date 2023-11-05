import uuid

from backend.game.players.player import Player
from backend.game.players.manual_move_player import ManualMovePlayer


class InteractivePlayerManager:
    """
    This Singleton class maintain all the istance of the Interactive Player:
    At this point of the development are only the REST one, maybe in the futrure there will be more
    """

    _instance: "InteractivePlayerManager" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init()
        return cls._instance
    
    def __init(self):   
        self.players = {}
    
    def add_user(self, user: ManualMovePlayer):
        self.players[user.getId()] = user

    def get_user(self, user_id: uuid) -> ManualMovePlayer | None:
        return self.players.get(user_id, None)
