from .singleton import SingletonMeta


class GameMapper(metaclass=SingletonMeta):
    """
    Maps the chatid to the game
    """

    _games: dict[int, int] = {}

    def add(self, chatid: int, game: int):
        self._games[chatid] = game

    def get(self, chatid: int):
        return self._games.get(chatid)

    def remove(self, chatid: int):
        self._games.pop(chatid)
