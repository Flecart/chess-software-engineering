from .singleton import SingletonMeta

class UserMapper(metaclass=SingletonMeta):
    """
    Used to Map chatid to userId
    """

    _paired_users: dict[str, str] = {}


    def add(self, user:str ,userId:str):
        self._paired_users[user] = userId

    def get(self, user: str):
        return self._paired_users.get(user)

    def remove(self, user: str):
        self._paired_users.pop(user)

