from .enums import EndReasons 

class BaseException(Exception):
    message = 'dark chess base exception'


class BaseArgException(BaseException):
    def __init__(self, *args, **kwargs):
        self.message = self.message.format(*args, **kwargs)
        super(BaseArgException, self).__init__(*args, **kwargs)

# engine exceptions
class OutOfBoardError(BaseException):
    message = 'coordinates are out of board'


class CellIsBusyError(BaseException):
    message = 'you cannot cut your figure'


class WrongMoveError(BaseException):
    message = 'wrong move'


class WrongFigureError(BaseException):
    message = 'you can move only your figures'


class WrongTurnError(BaseException):
    message = 'it is not your turn'


class NotFoundError(BaseException):
    message = 'figure not found'


class EndGame(BaseException):
    message = 'game is over'
    reason = None

class WhiteWon(EndGame):
    message = 'white player won'
    reason = EndReasons.CHECKMATE


class BlackWon(EndGame):
    message = 'black player won'
    reason = EndReasons.CHECKMATE


class Draw(EndGame):
    message = 'draw'
    reason = EndReasons.DRAW


# handlers exceptions
class GameNotFoundError(BaseException):
    message = 'game not found'


class GameNotStartedError(BaseException):
    message = 'game not started'

    def __init__(self, type=None, limit=None, token=None):
        self.type = type
        self.limit = limit
        self.token = token


class TooOftenRequestError(BaseArgException):
    message = 'too often requests, try again after {} seconds'


class VerifiedError(BaseException):
    message = 'your email is already verified'


class VerificationRequestError(BaseArgException):
    message = 'you must wait {} seconds to get new verification code'


class ValidationError(BaseArgException):
    message = '{} is not valid'


class ValidationRequiredError(ValidationError):
    message = '{} is required'


class ResetRequestError(BaseArgException):
    message = 'you must wait {} seconds to get new reset code'


# API exceptions
class APIException(BaseArgException):
    message = '{}'


class APIUnauthorized(APIException):
    message = 'not authorized'


class APIForbidden(APIException):
    message = 'forbidden'


class APINotFound(APIException):
    message = '{} not found'