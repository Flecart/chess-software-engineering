from .singleton import SingletonMeta

class UserMapper(metaclass=SingletonMeta):
    """
    Used to Map chatid to token
    """

    _paired_users: dict[int, str] = {}


    def add(self, chatid:int ,token:str):
        self._paired_users[chatid] = token

    def get(self, chatid: int):
        return self._paired_users.get(chatid)

    def remove(self, chatid: int):
        self._paired_users.pop(chatid)
