import chess
import numpy as np

from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import human
from open_spiel.python.bots import uniform_random
import pyspiel


from dataclasses import dataclass
from enum import StrEnum

class GameType(StrEnum):
  CHESS = 'chess'
  DARK_CHESS = 'dark_chess'

class Actions(StrEnum):
  MAKE_BEST_MOVE = "make_best_move" 
  LIST_MOVE = "list_move"
  MOVE = "move"

@dataclass
class GameStateInput:
  game_type:GameType
  fen: str
  action:list[str]
  parameters:str|None


class GameStateOutput:
  white_view:str
  black_view:str
  possible_moves: list[str]|None
  best_move:str|None
  fen:str




def _init_bot(bot_type, game):
  """Initializes a bot by type."""
  rng = np.random.RandomState(None)
  if bot_type == "mcts":
    evaluator = mcts.RandomRolloutEvaluator(1, rng)# How many rollouts to do.
    return mcts.MCTSBot(
        game,
        2, # UTC exploration constant
        1000, # max number of simulations
        evaluator,
        random_state=rng,
        solve=True, # use MCTS-Solver
        verbose=False)
  if bot_type == "random":
    return uniform_random.UniformRandomBot(1, rng)
  if bot_type == "human":
    return human.HumanBot()
  raise ValueError("Invalid bot type: %s" % bot_type)


def _best_move(game, state):
  bot = _init_bot('mcts',game)
  current_player = state.current_player()
  if state.is_chance_node():
    outcomes = state.chance_outcomes()
    action_list, prob_list = zip(*outcomes)
    action = np.random.choice(action_list, p=prob_list)
  elif state.is_simultaneous_node():
    raise ValueError("Game cannot have simultaneous nodes.")
  else:
    action = bot.step(state)

  return action,state.action_to_string(current_player,action)


def _create_state(game_name, fen=None):
  # it use undocumented new_initial_state(fen)
  # to generate from the fen in the case of chess
  # other variant use the fen parameter
  isChess = game_name == "chess"
  isValidFEN =  fen is not None
  params = {}
  if not isChess and isValidFEN:
    params["fen"] = fen
  game = pyspiel.load_game(game_name, params)
  state = game.new_initial_state(fen) if isChess and isValidFEN else game.new_initial_state()
  return game,state

  
def _legal_action_uci(game_type,state,fen):
  # This code is difficult because it relay on the specific implementation
  # of the libraries rather than the actual api
  board = chess.Board(fen)
  
  # transform the san to uci
  transform = lambda x: board.parse_san(state.action_to_string(x)).uci() 

  # kriegspiel is already in uci
  if game_type == 'kriegspiel':
    transform = lambda x:state.action_to_string(x)
  try:
    return list(map(transform,state.legal_actions()))
  except:
    # It changes the function which generate the move, to accept illegals moves 
    board.generate_legal_moves = board.generate_pseudo_legal_moves
    return list(map(transform,state.legal_actions()))

def _parse_action(state,action):
  pass


def _fen(state,game_type):
  if game_type == GameType.CHESS:
    return state.observation_string()
  else:
    return state.to_string()


def find(val,iter) -> int:
  for i,k in enumerate(iter):
    if k == val:
      return i
  return -1

def dispatch(input:GameStateInput) -> GameStateOutput:
  fen = input.fen
  game,state = _create_state(input.game_type,fen)
  out= GameStateOutput()
  if Actions.MOVE in input.action:
    ind = find(input.parameters,_legal_action_uci(input.game_type,state,fen))
    if ind ==-1:
      raise ValueError('Invalid Move')
    state.apply_action(state.legal_actions()[ind])
    fen =  _fen(state,input.game_type)
  if Actions.MAKE_BEST_MOVE in input.action:
    action,_ = _best_move(game,state) 
    state.apply_action(action)
    fen =  _fen(state,input.game_type)
  if Actions.LIST_MOVE in input.action:
    print(fen)
    out.possible_moves = _legal_action_uci(input.game_type,state,fen)

  out.white_view = state.observation_string(0)
  out.black_view = state.observation_string(1)
  out.fen =_fen(state,input.game_type) 
  return out





def main():
  game = GameStateInput("", "",[],None)
  game.fen = 'rnbqkbnr/ppp1pppp/8/1B1p4/4P3/8/PPPP1PPP/RNBQK1NR b KQkq - 0 0'
  game.game_type= 'dark_chess'
  game.action = [Actions.MAKE_BEST_MOVE,Actions.LIST_MOVE]
  game.game_type= 'kriegspiel'
  val = dispatch(game)
  print(vars(val))
  val = dispatch(game)
  print(vars(val))
  game.game_type= 'chess'
  val = dispatch(game)
  print(vars(val))
  

if __name__ == '__main__':
  main()