from .singleton import SingletonMeta

class GameMapper(metaclass=SingletonMeta): # Example of singleton, problablty will be removed
    """
    Maps the userId to the game
    """

    _games: dict[str, str] = {}

    def add(self, user:str ,game:str):
        self._games[user] = game

    def get(self, user: str):
        return self._games.get(user)

    def remove(self, user: str):
        self._games.pop(user)

