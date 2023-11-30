import asyncio
import datetime
from backend.config import Config
from backend.database.database import get_db_without_close
from backend.database.models import Game, User
from backend.game.v1_timer import Timer
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
    def __init__(self, game_creation: CreateGameRequest, fen: str = START_POSITION_FEN, moves: list[str] = []):
        session = get_db_without_close() 
        game = Game(
            white_player = None,
            black_player = None,
            moves = '',
            is_finish = False,
            winner = None ,
            fen=fen,
        )
        session.add_all([game])
        session.commit()
        self.__id = game.game_id
        session.close()

        self.__fen: str = fen
        self.__moves = moves.copy()

        self.__type: GameType = GameType(game_creation.type)
        game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.LIST_MOVE))

        self.__finished = game_state.finish
        self.__black_view = game_state.black_view
        self.__white_view = game_state.white_view

        self.__white_player: str|None = None
        self.__black_player: str|None = None

        self.__bot_player: bool = game_creation.against_bot
        self.__calculating: bool = False

        self.using_timer = game_creation.time != 0
        self.timer_white = Timer(datetime.timedelta(minutes=game_creation.time))
        self.timer_black = Timer(datetime.timedelta(minutes=game_creation.time))

    @property
    def id(self) -> str:
        return self.__id

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

        self._join_save()

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

    def _check_times_up(self)->bool:
        if not self.using_timer:
            return False
        if self.current_player == Color.WHITE:
            if self.timer_white.is_finished():
                return True
        elif self.current_player == Color.BLACK:
            if self.timer_black.is_finished():
                return True
        return False

    def _stop_timer(self):
        if self.current_player == Color.WHITE:
            self.timer_white.stop()
        else:
            self.timer_black.stop()

    def _start_timer(self):
        if self.current_player == Color.WHITE:
            self.timer_white.start()
        else:
            self.timer_black.start()


    def move(self, move: str) -> None:
        self._stop_timer()
        self.__finished = self._check_times_up() 

        if not self.__finished:
            game_state: GameStateOutput = engine.dispatch(self.__create_game_state_action(Actions.MOVE, move))
            self.__moves.append(move)
            self._start_timer()

            self.__fen = game_state.fen

            print("response fen", self.__fen, move)
            self.__finished = self.__finished or game_state.finish
            self.__black_view = game_state.black_view
            self.__white_view = game_state.white_view

        if self.__finished:
            self.save_and_update_elo()

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
            view=view,
            time_start_black=None if self.timer_black.start_time==None else self.timer_black.start_time.isoformat(), 
            time_start_white=None if self.timer_white.start_time==None else self.timer_white.start_time.isoformat(),
            time_left_black=str(self.timer_black.remaining_time),
            time_left_white=str(self.timer_white.remaining_time),
        )
    
    def get_bot_move(self, event_loop: asyncio.AbstractEventLoop) -> None:
        if self.__finished or (not self.__bot_player) or self.__calculating:
            return
        bot_color = self.get_player_color(_BOT_USERNAME)

        def make_bot_move(game: "ChessGame"):
            game.__calculating = True
            move = None
            available_moves = game.get_moves()
            while move not in available_moves:  # kriegspiel mode
                print(f"[bot player]: move {move} not in valid {available_moves}")
                move = game.get_best_move()
            game.move(move)
            game.__calculating = False
            from backend.game.v1_socket_manager import SocketManager
            event_loop.create_task(SocketManager().notify_opponent(game.__id, bot_color))

        
        if bot_color == self.current_player:
            import threading
            thread = threading.Thread(target=make_bot_move, args=(self,))
            thread.start()
            
    def save_and_update_elo(self):
        session = get_db_without_close()
        game = session.query(Game).filter(Game.game_id == self.__id).first()
        game.fen = self.__fen
        game.moves = ','.join(self.__moves)
        game.is_finish = self.__finished
        game.winner =  Color.BLACK if Color.BLACK == self.current_player else Color.WHITE
         
        if self.__finished and game.black_player is not None and game.white_player is not None:
            black = session.query(User).filter(User.user == game.black_player).first()
            white = session.query(User).filter(User.user == game.white_player).first()

            if game.winner == 'white':
                white.wins = white.wins + 1
                black.losses = black.losses + 1
            elif game.winner == 'black':
                black.wins = black.wins + 1
                white.losses = white.losses + 1

            game.black_points = black.rating
            game.white_points = white.rating
            white.rating = white.rating +\
                game.get_point_difference(white.user)
            black.rating = black.rating +\
                game.get_point_difference(black.user)
            
            session.add_all([black,white])
        session.add(game)
        session.commit()
        session.close()

    def __create_game_state_action(self, action:Actions, move: str|None=None) -> GameStateInput:
        return GameStateInput(self.__type, self.__fen, action, move)

    def _join_save(self):
        session = get_db_without_close()
        get_user = lambda user: session.query(User).\
                            filter(User.user == user).first()
        game = session.query(Game)\
            .filter(Game.game_id == self.__id).first()
        if self.__white_player is not None:
            user = get_user(self.__white_player)
            if user is not None:
                game.white_player = user.user

        if self.__black_player is not None:
            user = get_user(self.__black_player)
            if user is not None:
                game.black_player = user.user
        
        session.commit()
        session.close()