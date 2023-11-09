from dataclasses import dataclass
from enum import GameType

@dataclass
class GameStateInput:
  game_type:GameType
  fen: str
  action:list[str]
  move:str|None
  