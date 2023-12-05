from enum import StrEnum

class GameType(StrEnum):
    CHESS = 'chess'
    DARK_CHESS = 'dark_chess'
    KRIEGSPIEL = 'kriegspiel'

class Actions(StrEnum):
  MAKE_BEST_MOVE = "make_best_move" 
  LIST_MOVE = "list_move"
  MOVE = "move"
  GET_VALID_MOVE= "get_valid_move"
