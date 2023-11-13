from dataclasses import dataclass
from .enums import GameType,Actions

@dataclass
class GameStateInput:
  game_type:GameType
  fen: str
  action:Actions
  move:str|None
  
  