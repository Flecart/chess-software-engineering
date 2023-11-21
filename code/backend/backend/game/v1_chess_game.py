import asyncio
from backend.config import Config
from backend.routes.game.data import CreateGameRequest, GameStatusResponse
from backend.bot.data.game_state_input import GameStateInput
from backend.bot.data.game_state_output import GameStateOutput
from backend.bot.data.enums import Actions

from backend.bot.data.enums import GameType
from .utils import START_POSITION_FEN, Color 
import backend.bot.mcts as engine


_BOT_USERNAME = Config()['bot']

class ChessGame():
    # TODO: definisci la tipologia di mosse
    def __init__(self,id:int, game_creation: CreateGameRequest, fen: str = START_POSITION_FEN, moves: list[str] = []):
        self.__id:int = id
        self.__fen: str = fen
        self.__moves = moves

        # TODO(ang): usa informazioni di game_creation per settare i giocatori
        # e la tipologia di gioco
        self.__type: GameType = GameType(game_creation.type)

        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.LIST_MOVE))

        self.__finished = game_state.finish
        self.__black_view = game_state.black_view
        self.__white_view = game_state.white_view

        self.__white_player: str|None = None
        self.__black_player: str|None = None

        self.__bot_player:bool = game_creation.against_bot
        self.__calculating:bool = False

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

    def is_current_player(self, username: str) -> bool:
        color = self.current_player
        if color == Color.WHITE and self.__white_player == username:
            return True
        
        if color == Color.BLACK and self.__black_player == username:
            return True
        
        return False

    def join(self, user: str, color: Color) -> None:
        if color == Color.WHITE:
            if self.__white_player is not None:
                raise ValueError("White color has already joined")
            self.__white_player = user
        elif color == Color.BLACK:
            if self.__black_player is not None:
                raise ValueError("Black color has already joined")
            self.__black_player = user
        else:
            raise ValueError("color must be white or black")

        if self.__bot_player:
            if self.__black_player is None:
                self.__black_player = _BOT_USERNAME
            elif self.__white_player is None:
                self.__white_player = _BOT_USERNAME
            else:
                raise ValueError("Bot player can't join a game with two players")


    def get_player_color(self, username: str) -> Color | None:
        """
        Get the color of a player from its username.
        """
        if self.__white_player == username:
            return Color.WHITE
        elif self.__black_player == username:
            return Color.BLACK
        else:
            return None

    def get_moves(self) -> None:
        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.LIST_MOVE, None))
        return game_state.possible_moves
    
    def get_best_move(self) -> str:
        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.MAKE_BEST_MOVE, None))
        return game_state.best_move

    def move(self, move: str) -> None:
        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.MOVE, move))
        self.__moves.append(move)
        self.__fen = game_state.fen
        self.__finished = game_state.finish

        self.__black_view = game_state.black_view
        self.__white_view = game_state.white_view

    def get_player_response(self,
                            color: Color,
                            possible_moves: list[str] | None = None,
                            move_made: str | None = None
    ) -> GameStatusResponse:
        view = ''
        if color == Color.BLACK:
            view = self.__black_view
        elif color == Color.WHITE:
            view = self.__white_view
        else:
            raise ValueError('Invalid color')

        return GameStatusResponse(
            ended= self.__finished,
            move_made = move_made, 
            possible_moves=  possible_moves,
            turn = self.current_player.name.__str__().lower(),
            view=view
        )
    
    def get_bot_move(self,event_loop:asyncio.AbstractEventLoop) -> None:
        if self.__finished or (not self.__bot_player) \
              or self.__calculating:
            return
        bot_color = self.get_player_color(_BOT_USERNAME)


        def make_bot_move(game):
            game.__calculating = True
            move = game.get_best_move()
            game.move(move[0])
            game.__calculating = False
            from backend.game.v1_socket_manager import SocketManager
            event_loop.create_task(SocketManager().notify_opponent(game.__id, bot_color))

        
        if bot_color == self.current_player:
            import threading
            thread = threading.Thread(target=make_bot_move, args=(self,))
            thread.start()
            


    def __create_game_state_action(self, action:Actions, move: str|None=None) -> GameStateInput:
        return GameStateInput(self.__type, self.__fen, action, move)
    