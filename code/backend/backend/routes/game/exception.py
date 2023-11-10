class JoinException(Exception):
    def __init__(self, name: str= "temp",game_id:int =1):
        self.name = name
        self.game_id = game_id


register_exception(JoinException)