import socketio 
import random
import uuid
from backend.bot.data.game_state_input import GameStateInput
from backend.bot.data.enums import Actions
from backend.bot.mcts import dispatch
from backend.config import Config
from enum import StrEnum, auto
from backend.game.utils import KRIEGSPIEL_INVALID_MOVE

class DarkBoardStates(StrEnum):
    WAITING_FOR_MOVE = auto()
    WAITING_FOR_COMPUTER_BEST_MOVE  = auto()
    GAME_OVER  = auto()
    WAITING_FOR_OPPONENT_MOVE = auto()
    ERROR = auto()

game_type = 'kriegspiel'
class DarkBoard():

    def __init__(self, ):
        self.__fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0'
        self._state = DarkBoardStates.GAME_OVER
        self.__old_fen: str | None = None
        self.sio = socketio.Client()
        self.messages = []
        self.last_interaction = None
        self.error_message = None


        # Socket events
        @self.sio.event
        def connect():
            self._state = DarkBoardStates.WAITING_FOR_MOVE
            self.sio.emit("ready")
        
        @self.sio.event
        def game_over(pgn):
            self._state = DarkBoardStates.GAME_OVER
        
        @self.sio.event
        def read_message(message):
            print('message', message)
            self.messages.append(message)
            if 'White\'s turn;' in  message:
                self._state = DarkBoardStates.WAITING_FOR_MOVE
                print("It's my turn!")
            
        
        @self.sio.event
        def chessboard_changed(fen):
            self.__old_fen = self.__fen
            if fen != self.__fen:
                self.__fen = fen

        @self.sio.event
        def error(err):
            self._state = DarkBoardStates.ERROR
            self.error_message = 'Error from the other server '+err

        @self.sio.event
        def disconnect():
            print("Disconneted")
            self._state = DarkBoardStates.ERROR
            self.error_message = 'The other server has disconnected'

    @property
    def fen(self):
        return self.__fen

    def connect(self, connection_string: str = Config()['URL_KRIEGSPER']): #TODO sosituirlo con un env
        # const connectionPayloadDeveloper f 0 username, .TestBot., gameType, .developer., token: .bec635e710d6cdd5t3d3aa2b1c2e7007e45881eaf5d4g6b. 
        # 5 const connectionPayload f username: .gianlo., gameType: .darkboard., room: .test., 


        connection_payload = {
            "username": "checkmates-"+str(random.randint(0,1000)),
            "gameType": "developer",
            "token": "bec635e710d6cdd5t3d3aa2b1c2e7007e45881eaf5d4g6b"
        }

        query_string = "&".join([f"{key}={value}" for key, value in connection_payload.items()])

        self.sio.connect(connection_string + query_string)

    def send_move(self, move: str):
        """ A move in algebraic notation, e.g. e2e4
        """
        assert len(move) == 4, "Invalid move"
        assert move[0].isalpha() and move[1].isdigit() and move[2].isalpha() and move[3].isdigit(), "Invalid move"

        self.sio.emit("make_move", DarkBoard.move_to_san(self.__fen, move))

    def is_move_valid(self, move: str) -> bool:
        """ Check if a move is valid
        
        """
        return self.__fen != self.__old_fen

    # TODO: might be a good idea to move these methods to util file
    @staticmethod
    def move_to_san(fen, move):
        # Convert FEN string to list of squares
        squares = DarkBoard.fen_to_squares(fen)
        
        # Parse the move
        from_square, to_square = move[0:2], move[2:]

        from_rank, from_file = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
        
        # Get the piece moving
        piece = squares[from_rank][from_file]
        
        if piece.lower() == 'p' :
            return move
        
        print(f"DEbuG: piece {piece}{move}")
        return f"{piece}{move}"
    
    @staticmethod
    def fen_to_squares(fen: str) -> list[list[str]]:
        """ Convert FEN string to a list of lists representing the chess board
        
        """
        # 
        curr_board: list[str] = [list(row) for row in fen.split(" ")[0].split('/')]
        final_board: list[list[str]] = [["."] * 8 for _ in range(8)]

        for i in range(len(curr_board)):
            offset = 0
            for j in range(len(curr_board[i])):
                if not curr_board[i][j].isdigit():
                    final_board[i][j + offset] = curr_board[i][j]
                else:
                    offset += int(curr_board[i][j]) - 1

        return final_board
    
    @property
    def state(self):
        return self._state

    def make_move(self,move):
        input = GameStateInput(game_type,self.fen,Actions.MOVE,move)    
        return dispatch(input)
    
    def best_move(self):
        invalid_counter = 0
        # Temporary value just used not to infinite loop
        while invalid_counter < 2:
            print("Waiting for best move", invalid_counter)
            self._state = DarkBoardStates.WAITING_FOR_COMPUTER_BEST_MOVE
            input = GameStateInput(game_type, self.fen, Actions.MAKE_BEST_MOVE, None)    
            state = dispatch(input)
            if state.white_view != KRIEGSPIEL_INVALID_MOVE or state.black_view != KRIEGSPIEL_INVALID_MOVE:
                invalid_counter += 1
                continue
            print("Best move", state.best_move)
            return state.best_move[0]
            
        input = GameStateInput(game_type, self.fen, Actions.GET_VALID_MOVE, None)    
        state = dispatch(input)
        print("Best move", state.best_move)
        return state.best_move


class DarkBoardSingleton:
    _instance = None
   
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init()
        return cls._instance
    
    def __init(self):
        self.darkboard = DarkBoard()
        
    def create_game(self):
        if self.darkboard is None or self.darkboard.state == DarkBoardStates.GAME_OVER or self.darkboard.state == DarkBoardStates.ERROR:
            self.darkboard = DarkBoard()
            self.darkboard.connect()
    
    @property
    def get_fen(self):
        return self.darkboard.fen

    @property
    def get_error_message(self):
        return self.darkboard.error_message

    @property
    def get_message(self):
        return self.darkboard.messages

    @property
    def get_state(self):
        return self.darkboard.state

    def make_best_move(self) :
        if self.get_state == DarkBoardStates.WAITING_FOR_MOVE :
            best = self.darkboard.best_move()
            self.darkboard.send_move(best)

