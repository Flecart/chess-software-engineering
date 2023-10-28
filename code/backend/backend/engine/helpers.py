#import uuid
#from hashlib import md5


from .enums import Colors


def onBoard(x: int, y: int) -> bool:
    if 1 <= x <= 8 and 1 <= y <= 8:
        return True
    return False

# TODO: these coors are not standard format, should use PGN format, see #9
def pos2coors(x: int, y: int) -> str:
   if not (isinstance(x, int) and isinstance(y, int)):
       raise TypeError
   if not onBoard(x, y):
       raise ValueError
   return '{}{}'.format('abcdefgh'[x - 1], y)

def coors2pos(coors: str) -> tuple[int, int]:
    if len(coors) != 2:
        raise ValueError
    x, y = coors[0].lower(), int(coors[1])
    return ('abcdefgh'.index(x) + 1, y)

def invert_color(color: Colors) -> Colors:
    if color == Colors.WHITE:
        return Colors.BLACK
    return Colors.WHITE


def validate_move_format(move: str) -> bool:
    """ Just a quick way to check the move format, 
    
    Example correct format:
    e2e4
    Meaning: move piece on e2 to e4.
    The correctness check should be done by the engine
    """
    if len(move) != 4:
        return False
    
    letter_set = "abcdefgh"
    number_set = "12345678"

    if not move[0] in letter_set or not move[2] in letter_set:
        return False
    
    if not move[1] in number_set or not move[3] in number_set:
        return False
    
    return True