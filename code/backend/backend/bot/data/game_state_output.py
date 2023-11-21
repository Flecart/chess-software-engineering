from dataclasses import dataclass

class GameStateOutput:
  white_view: str
  black_view: str
  possible_moves: list[str] | None = None
  best_move: str | None = None
  fen: str 
  finish: bool

