from .singleton import SingletonMeta

class ValidMovesMapper(metaclass=SingletonMeta):
    """
    Maps the valid moves for each chatid
    """

    _valid_moves: dict[int, list[str]] = {}

    def add(self, chatid: int, moves: list[str]):
        self._valid_moves[chatid] = moves

    def get(self, chatid: int):
        return self._valid_moves.get(chatid)

    def remove(self, chatid: int):
        self._valid_moves.pop(chatid)
