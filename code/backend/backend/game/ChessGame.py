class ChessGame:
    moves:list[str]

    def __init__(self):
        self.moves = []

    def add_move(self, move:str):
        self.moves.append(move)