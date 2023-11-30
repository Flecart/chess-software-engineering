import time
import socketio 
import sys
import random
import uuid
from backend.bot.data.enums import Actions

from backend.bot.data.game_state_input import GameStateInput
from mcts  import dispatch


def fen_to_squares(fen):
    # Convert FEN string to a list of lists representing the chess board
    board = [list(row) for row in fen.split()[0].split('/')]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].isdigit():
                # If it's a number, replace it with that many empty squares
                for k in range(int(board[i][j])):
                    board[i][j+k] = '.'
    return [square for row in board for square in row]


def move_to_san(fen, move):
    # Convert FEN string to list of squares
    squares = fen_to_squares(fen)
    
    # Parse the move
    from_square, to_square = move[0:2], move[2:]
    breakpoint()
    from_rank, from_file = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
    
    # Get the piece moving
    piece = squares[from_rank * 8 + from_file]
    
    if piece.lower() == 'p' :
        return move
    
    return f"{piece}{move}"

connection_payload = {
    "username": "gianlo"+str(random.randint(0,1000)),
    "gameType": "darkboard",
    "room": uuid.uuid4().hex
}

game_type= 'kriegspiel'

def make_move(fen,move):
    input = GameStateInput(game_type,fen,Actions.MOVE,move)    
    return dispatch(input)
 
def best_move(fen):
    input = GameStateInput(game_type,fen,Actions.MAKE_BEST_MOVE,None)    
    return dispatch(input).best_move[0]
 

# Main function
def main():
    game = GameStateInput("", "",[],None)
    print("Connecting...")
    sio = socketio.Client()
    # Connection to the server


    # query encode a json
    query_string = "&".join([f"{key}={value}" for key, value in connection_payload.items()])

    ## add url parameter in the connection_payload to the url
    url = 'http://192.168.224.22:8085/?' +query_string
    sio.connect(url)

    # Socket events
    @sio.event
    def connect():
        print("Connected!")
        # Chess instance to keep track of the game
        sio.emit("start_game")
    
    @sio.event
    def game_over(pgn):
        print("Game over!")
        sys.exit()
    
    @sio.event
    def read_message(message):
        print('prova '+message)
    
    @sio.event
    def chessboard_changed(fen):
        fen = fen
        print('arrived fen ', fen)
    
    @sio.event
    def error(err):
        print("Error: ", err)
        sys.exit(1)

    @sio.event
    def disconnect():
        print("Disconnected!")
        sys.exit()

    print("creating game state")
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    while True:
        command = input("Move by bot ")
        if command == "move":
            my_move = move_to_san(fen,best_move(fen))
            print(my_move)
            sio.emit("make_move", my_move)
        else:
            print("Invalid command!")
    print("Exiting...")


if __name__ == '__main__':
    main()



