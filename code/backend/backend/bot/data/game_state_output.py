from dataclasses import dataclass

class GameStateOutput:
  white_view:str
  black_view:str
  possible_moves: list[str]|None
  best_move:str|None
  fen:str
  finish:bool

