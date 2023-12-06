help_text = "Welcome to the game! \n\
        I'm a bot that let's you play Dark chess with your friends! \n\
        Run /newGame <time> starts a new game, the default is 10 minutes\n\
        Run /leave to leave the current game \n\
        Run /vote <move> to give your preference to the next move\n\
        Run /rules to know more about Dark Chess and the Vote Mode"


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

Also this bot permit you to play Dark Chess cooperating with your friends:
- Every group member participate to choose witch move do
- The players has to think and debate on moves
- Then the most voted move is played
See https://www.chess.com/blog/13pax/vote-chess-faqs-tips-and-suggestion for more information
"""
