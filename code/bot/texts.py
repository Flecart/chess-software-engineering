
# TODO modify this
help_text = "Welcome to the game! \n\
        I'm a bot that let's you play Dark chess with your friends! \n\
        Using the current version you will have a text version of the game, \n\
        Run /rules to see the rules of dark chess game. \n\
        Run /leave to be able to start a new game after the current ended. You can leave the room only if the game finished. \n\
        Run /legend to see the legend of the FEN format for the game. \n\
        Run /createGameAgainstBot to create a new game and start playing!"


# TODO modify this
rules_text = """
The rules of dark chess are the same of normal chess, with the following differences:
- There is no check or checkmate. Each player can freely move his/her king to a check position.
- The player who captures the opponent's king, wins the game.

Furthermore this version is information incomplete.
The squares that are visible to the player must follow one of these conditions:
- A player's piece stands on that square.
- The player can move a piece to that square. This means that he/she can see empty squares that he/she can move to, or an opponent's piece that he/she can capture.
- The square is directly in front of one of player's pawns or it is an adjacent forward diagonal from one of player's pawns.
See https://brainking.com/en/GameRules for more information
"""


legend_text = """
Upper case is white player
Lower case is black player
K is king
Q is queen
R is rook
B is bishop
N is knight
P is pawn
. is empty square
X is not visible square
"""
