import chess
import numpy as np

from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import human
from open_spiel.python.bots import uniform_random
import pyspiel

from backend.bot.data.enums import GameType,Actions
from backend.bot.data.game_state_input import GameStateInput
from backend.bot.data.game_state_output import GameStateOutput
from backend.bot.data.MCST_player_config import MCSTPlayerConfig


def _init_bot(bot_type, game,config):
  """Initializes a bot by type."""
  rng = np.random.RandomState(None)
  if bot_type == "mcts":
    evaluator = mcts.RandomRolloutEvaluator(config.roll_outs, rng)# How many rollouts to do.
    return mcts.MCTSBot(
        game,
        config.utc, # UTC exploration constant
        config.max_sim, # max number of simulations
        evaluator,
        random_state=rng,
        solve=True, # use MCTS-Solver
        verbose=False)
  if bot_type == "random":
    return uniform_random.UniformRandomBot(1, rng)
  if bot_type == "human":
    return human.HumanBot()
  raise ValueError("Invalid bot type: %s" % bot_type)


def _get_best_move(game, state):
  bot = _init_bot('mcts',game,MCSTPlayerConfig())
  if state.is_chance_node():
    outcomes = state.chance_outcomes()
    action_list, prob_list = zip(*outcomes)
    action = np.random.choice(action_list, p=prob_list)
  elif state.is_simultaneous_node():
    raise ValueError("Game cannot have simultaneous nodes.")
  else:
    action = bot.step(state)

  return action


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



def _legal_action_to_uci(game_type,state,fen):
  return _actions_to_uci(game_type,state,fen,state.legal_actions())

def action_to_uci(game_type,state,fen,action):
  return _actions_to_uci(game_type,state,fen,[action])


def _check_castling(state:str):
  if state.startswith('O-O-O'):
    return 'e1c1'
  if state.startswith('O-O'):
    return 'e1g1'
  if state.startswith('o-o-o'):
    return 'e8c8'
  if state.startswith('o-o'):
    return 'e8g8'
  raise ValueError('Invalid Move')

  
def _actions_to_uci(game_type,state,fen,actions=None):
  # This code is difficult because it relay on the specific implementation
  # of the libraries rather than the actual api
  board = chess.Board(fen)
  
  # transform the san to uci

  transform = lambda x:board.parse_san(state.action_to_string(x)).uci()
  # kriegspiel is already in uci
  if game_type == 'kriegspiel':
    transform = lambda x:state.action_to_string(x)
  try:
    return list(map(transform,actions))
  except:
    # It changes the function which generate the move, to accept illegals moves 
    board.generate_legal_moves = board.generate_pseudo_legal_moves
    def _handle_check_castling(action):
      try:
        return transform(action)
      except:
        return _check_castling(state.action_to_string(action))

    return list(map(transform,actions))


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

def dispatch(game_state_input:GameStateInput) -> GameStateOutput:
  fen = game_state_input.fen
  game,state = _create_state(game_state_input.game_type,fen)
  out= GameStateOutput()

  match game_state_input.action:
    case Actions.MOVE:
      ind = find(game_state_input.parameters,_legal_action_to_uci(game_state_input.game_type,state,fen))
      if ind ==-1:
        raise ValueError('Invalid Move')
      state.apply_action(state.legal_actions()[ind])
      fen =  _fen(state,game_state_input.game_type)

    case Actions.MAKE_BEST_MOVE:
      action = _get_best_move(game,state) 
      out.best_move = action_to_uci(game_state_input.game_type,state,fen,action)
      state.apply_action(action)
      fen =  _fen(state,game_state_input.game_type)
    
    case Actions.LIST_MOVE:
      out.possible_moves = _legal_action_to_uci(game_state_input.game_type,state,fen)
    
  out.finish = state.is_terminal()
  out.white_view = state.observation_string(0)
  out.black_view = state.observation_string(1)
  out.fen =_fen(state,game_state_input.game_type) 
  return out


def _print_game_state_output(out:GameStateOutput):
  print('white_view',out.white_view)
  print('black_view',out.black_view)
  print('possible_moves',out.possible_moves)
  print('best_move',out.best_move)
  print('fen',out.fen)


def main():
  game = GameStateInput("", "",[],None)
  game.fen = '4r1k1/8/8/8/8/8/8/R3K2R w KQ - 0 1'
  game.game_type= 'dark_chess'
  game.parameters="c8d7"
  game.action = Actions.LIST_MOVE
  val = dispatch(game)
  _print_game_state_output(val)
  

if __name__ == '__main__':
  main()
