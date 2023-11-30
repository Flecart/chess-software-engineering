import socketio 
import random
import uuid

class DarkBoard():
    def __init__(self, ):
        self.__fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0'
        self.__old_fen: str | None = None
        self.sio = socketio.Client()


        # Socket events
        @self.sio.event
        def connect():
            print("Connected!")
            # Chess instance to keep track of the game
            self.sio.emit("start_game")
        
        @self.sio.event
        def game_over(pgn):
            print("Game over!")
        
        @self.sio.event
        def read_message(message):
            print('prova '+ message)
        
        @self.sio.event
        def chessboard_changed(fen):
            self.__old_fen = self.__fen
            self.__fen = fen
            print('arrived fen ', fen)
        
        @self.sio.event
        def error(err):
            print("Error: ", err)

        @self.sio.event
        def disconnect():
            print("Disconnected!")

    @property
    def fen(self):
        return self.__fen

    def connect(self, connection_string: str = 'http://0.0.0.0:8085/?'):

        connection_payload = {
            "username": "gianlo"+str(random.randint(0,1000)),
            "gameType": "darkboard",
            "room": uuid.uuid4().hex
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
            for j in range(len(curr_board[i])):
                if not curr_board[i][j].isdigit():
                    final_board[i][j] = curr_board[i][j]

        print(final_board)
        return final_board
    
if __name__ == "__main__":
    from backend.bot.data.game_state_input import GameStateInput
    from backend.bot.data.enums import Actions
    from mcts import dispatch

    game_type = 'kriegspiel'

    def make_move(fen,move):
        input = GameStateInput(game_type,fen,Actions.MOVE,move)    
        return dispatch(input)
    
    def best_move(fen):
        input = GameStateInput(game_type,fen,Actions.MAKE_BEST_MOVE,None)    
        return dispatch(input).best_move[0]
 
    print("creating game state")

    darkboard = DarkBoard()
    darkboard.connect()

    while True:
        command = input("Command: ")
        if command == "move":
            # NOTA: per risolvere il problema del stateful, si potrebbe estendere dispatch ad accettare un GameState di OpenSpiel,
            # se ha il gamestate invece di stringa, prova a runnare in altro modo per dire.

            my_move = best_move(darkboard.fen)
            darkboard.send_move(my_move)
        else:
            print("Invalid command!")