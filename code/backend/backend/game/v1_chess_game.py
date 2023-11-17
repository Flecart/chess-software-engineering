from fastapi import WebSocket

from backend.routes.game.data import CreateGameRequest, GameStatusResponse
from backend.bot.data.game_state_input import GameStateInput
from backend.bot.data.game_state_output import GameStateOutput
from backend.bot.data.enums import Actions

from .utils import START_POSITION_FEN, Color, GameTypes
import backend.bot.mcts as engine

from pydantic import BaseModel
from typing import Literal


# TODO: refactor, move me to response and answer format folder
class GameResponse(BaseModel):
    kind: Literal["status"] # add with other types
    data: GameStatusResponse

class ChessGame():
    # TODO: definisci la tipologia di mosse
    def __init__(self, game_creation: CreateGameRequest, fen: str = START_POSITION_FEN, moves: list[str] = []):
        self.__fen: str = fen
        self.__finished: bool = False
        self.__moves = moves

        # TODO(ang): usa informazioni di game_creation per settare i giocatori
        # e la tipologia di gioco
        self.__type: GameTypes = GameTypes(game_creation.type)

        self.__black_view: str|None = None
        self.__white_view: str|None = None

        self.__white_socket: WebSocket|None = None
        self.__black_socket: WebSocket|None = None
        

    @property
    def fen(self) -> str:
        return self.__fen
    
    @property
    def moves(self) -> list[str]:
        return self.__moves
    
    @property
    def white_view(self) -> str:
        return self.__white_view
    
    @property
    def black_view(self) -> str:
        return self.__black_view

    @property
    def current_player(self) -> Color:
        return Color.WHITE if len(self.__moves) % 2 == 0 else Color.BLACK

    def join(self, socket: WebSocket, color: Color) -> None:
        if color == Color.WHITE:
            self.__white_socket = socket
        elif color == Color.BLACK:
            self.__black_socket = socket
        else:
            raise ValueError("color must be white or black")

    def broadcast(self) -> None:
        """
        Sends the current state to both players
        """
        if self.__white_socket is None or self.__black_socket is None:
            raise ValueError("players not connected")
        
        self.__white_socket.send_json(
            GameResponse(kind="status", data=self.__make_status_response(Color.WHITE))
        )
        self.__black_socket.send_json(
            GameResponse(kind="status", data=self.__make_status_response(Color.BLACK))
        )

    def get_moves(self) -> None:
        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.LIST_MOVE,None))
        return game_state.possible_moves
    
    def get_best_move(self) -> str:
        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.MAKE_BEST_MOVE,None))
        return game_state.best_move

    def move(self, move: str) -> None:
        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.MOVE, move))
        self.__moves.append(move)
        self.__fen = game_state.fen
        self.__finished = game_state.finish

        self.__black_view = game_state.black_view
        self.__white_view = game_state.white_view

    def __create_game_state_action(self, action:Actions, move: str|None) -> GameStateInput:
        return GameStateInput(self.__fen, self.__type,action, move)
    
    def __make_status_response(self, color: Color) -> GameStatusResponse:
        return GameStatusResponse(
            self.__fen,
            self.__finished,
            None,
            self.__white_view if color == Color.WHITE else self.__black_view,
            self.__moves[-1] if len(self.__moves) > 0 else None,
        )
