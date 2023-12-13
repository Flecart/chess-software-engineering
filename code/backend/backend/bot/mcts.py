import chess
import numpy as np
from copy import deepcopy
import random

from open_spiel.python.algorithms import mcts
from open_spiel.python.bots import human
from open_spiel.python.bots import uniform_random
import pyspiel

from backend.bot.data.enums import GameType, Actions
from backend.bot.data.game_state_input import GameStateInput
from backend.bot.data.game_state_output import GameStateOutput
from backend.bot.data.MCST_player_config import MCSTPlayerConfig
from backend.game.utils import KRIEGSPIEL_INVALID_MOVE


def _init_bot(bot_type, game, config):
    """Initializes a bot by type."""
    rng = np.random.RandomState(None)
    if bot_type == "mcts":
        evaluator = mcts.RandomRolloutEvaluator(
            config.roll_outs, rng
        )  # How many rollouts to do.
        return mcts.MCTSBot(
            game,
            config.utc,  # UTC exploration constant
            config.max_sim,  # max number of simulations
            evaluator,
            random_state=rng,
            solve=True,  # use MCTS-Solver
            verbose=False,
        )
    #  if bot_type == "random":
    #  return uniform_random.UniformRandomBot(1, rng)
    # if bot_type == "human":
    #  return human.HumanBot()
    raise ValueError("Invalid bot type: %s" % bot_type)


def _get_best_move(game, state):
    bot = _init_bot("mcts", game, MCSTPlayerConfig())
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
    isValidFEN = fen is not None
    params = {}
    if not isChess and isValidFEN:
        params["fen"] = fen

    game = pyspiel.load_game(game_name, params)
    state = (
        game.new_initial_state(fen)
        if isChess and isValidFEN
        else game.new_initial_state()
    )
    return game, state


def _legal_action_to_uci(game_type, state, fen):
    return _actions_to_uci(game_type, state, fen, state.legal_actions())


def action_to_uci(game_type, state, fen, action):
    return _actions_to_uci(game_type, state, fen, [action])[0]


def _check_castling(state: str):
    if state.startswith("O-O-O"):
        return "e1c1"
    if state.startswith("O-O"):
        return "e1g1"
    if state.startswith("o-o-o"):
        return "e8c8"
    if state.startswith("o-o"):
        return "e8g8"
    raise ValueError("Invalid Move")


def _actions_to_uci(game_type, state, fen, actions=None):
    # This code is difficult because it relays on the specific implementation
    # of the libraries rather than the actual api
    board = chess.Board(fen)

    # transform the san to uci
    transform = lambda x: board.parse_san(state.action_to_string(x)).uci()
    if game_type == "kriegspiel":
        # kriegspiel is already in uci
        transform = lambda x: state.action_to_string(x)

    try:
        return list(map(transform, actions))
    except:
        # This changes the function used to generate the move, in order to accept illegals moves
        board.generate_legal_moves = board.generate_pseudo_legal_moves

        def _handle_check_castling(action):
            try:
                return transform(action)
            except:
                return _check_castling(state.action_to_string(action))

        return list(map(_handle_check_castling, actions))


def _fen(state, game_type):
    if game_type == GameType.CHESS:
        return state.observation_string()
    else:
        return state.to_string()


def _custom_observation_string(state, player_id: int, game_type: str):
    """
    This function is just a quick way to implement the right view, but it is not mantainable,
    TODO: refactor me, use openspiel api somehow
    """

    if game_type != GameType.KRIEGSPIEL:
        return state.observation_string(player_id)

    # kriegspiel
    fen = state.to_string()
    splitted_fen = fen.split(" ")

    first_part, rest = splitted_fen[0], splitted_fen[1:]

    all_table = [["."] * 8 for _ in range(8)]
    checker = (
        lambda x: x.isalpha() and x.islower()
        if player_id == 0
        else x.isalpha() and x.isupper()
    )

    # compute correct view for the player
    rows = first_part.split("/")
    for i in range(len(rows)):
        offsets = 0
        for j in range(len(rows[i])):
            if rows[i][j].isdigit():
                for k in range(int(rows[i][j])):
                    all_table[i][offsets + k] = "."
                offsets += int(rows[i][j])
            elif checker(rows[i][j]):
                all_table[i][offsets] = rows[i][j]
                offsets += 1
            else:
                all_table[i][offsets] = "."
                offsets += 1

    return "/".join(["".join(row) for row in all_table]) + " " + " ".join(rest)


def _create_chat_bot_message(state, player_id: int, input_struct: GameStateInput):
    raise NotImplementedError("Not implemented yet")


def _create_observation_string(state, player_id: int, input_struct: GameStateInput):
    """
    Parameters
    ----------
    state : pyspiel.State
      The state of the game.

    player_id : int
      The player for which the observation string is generated.
    """

    match input_struct.game_type:
        case GameType.CHESS:
            return state.observation_string(player_id)
        case GameType.KRIEGSPIEL:
            return state.observation_string(player_id)
        case GameType.DARK_CHESS:
            return ""
    # return _create_chat_bot_message(state, player_id, input_struct)


def dispatch(game_state_input: GameStateInput) -> GameStateOutput:
    fen = game_state_input.fen
    game, state = _create_state(game_state_input.game_type, fen)
    out = GameStateOutput()

    match game_state_input.action:
        case Actions.MOVE:
            try:
                index = _legal_action_to_uci(
                    game_state_input.game_type, state, fen
                ).index(game_state_input.move)
            except ValueError:
                raise ValueError("Invalid Move")

            state.apply_action(state.legal_actions()[index])
            fen = _fen(state, game_state_input.game_type)

        case Actions.MAKE_BEST_MOVE:
            action = _get_best_move(game, state)
            out.best_move = action_to_uci(
                game_state_input.game_type, state, fen, action
            )
            state.apply_action(action)
            fen = _fen(state, game_state_input.game_type)

        case Actions.LIST_MOVE:
            out.possible_moves = _legal_action_to_uci(
                game_state_input.game_type, state, fen
            )

        case Actions.GET_VALID_MOVE:
            # make shuffle
            actions = state.legal_actions()
            random.shuffle(actions)
            for i in actions:
                _, newState = _create_state(game_state_input.game_type, fen)
                # newState = deepcopy(state)
                newState.apply_action(i)
                if newState.observation_string(1) == KRIEGSPIEL_INVALID_MOVE:
                    continue
                if newState.observation_string(0) == KRIEGSPIEL_INVALID_MOVE:
                    continue
                out.best_move = action_to_uci(game_state_input.game_type, state, fen, i)
                state = newState
                break

    # TODO: you should refactor this maybe with builder pattern??
    out.fen = _fen(state, game_state_input.game_type)


    out.finish = state.is_terminal()
    out.white_view = _custom_observation_string(state, 1, game_state_input.game_type)
    out.black_view = _custom_observation_string(state, 0, game_state_input.game_type)
    if game_state_input.game_type == GameType.KRIEGSPIEL:
        _, statechess = _create_state(GameType.CHESS, fen)
        out.finish = statechess.is_terminal()

    player_id = 0 if fen.split(" ")[1] == "w" else 1
    out.general_message = _create_observation_string(state, player_id, game_state_input)

    return out

if __name__ =='__main__':
    fen = "1n1r2k1/1p2b1q1/3B3p/5p2/b7/4K3/r7/q7 b - - 2 41"
    _, statechess = _create_state(GameType.CHESS, fen)
    out= statechess.is_terminal()
    print(out)

    