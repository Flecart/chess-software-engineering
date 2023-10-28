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


#def encrypt_password(password):
#    pass_md5 = md5(password.encode()).hexdigest()
#    return md5((pass_md5 + config.PASSWORD_SALT).encode()).hexdigest()
#
#
#def generate_token(short=False):
#    token = uuid.uuid4().hex
#    if short:
#        return token[:config.TOKEN_SHORT_LENGTH]
#    return token
#
#
#def with_context(data):
#    context = {
#        'site_url': config.SITE_URL,
#    }
#    context.update(data)
#    return context
#
#
#def get_queue_name(prefix):
#    return '{}_{}'.format(prefix, config.GAME_QUEUE_NAME)
#
#
#def get_prefix(game_type, game_limit=None):
#
#def get_request_arg(request, name):
    return request.form.get(name) or (request.json or {}).get(name)