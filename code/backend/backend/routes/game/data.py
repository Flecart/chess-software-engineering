from pydantic import BaseModel
from typing import Literal


class CreateGameRequest(BaseModel):
    against_bot: bool = True
    type: str = "dark_chess"  # default value
    time: int = 0


class GameStatusResponse(BaseModel):
    ended: bool
    possible_moves: list[str] | None = None
    view: str
    move_made: str | None
    turn: Literal["white", "black"]
    using_timer: bool
    time_left_white: str | None  # should also be added from when
    time_left_black: str | None
    time_start_white: str | None
    time_start_black: str | None
    message: list[str] = []  # currently (30 Nov) used in Kriegspiel for Umpire messages


class WebsocketRequests(BaseModel):
    kind: Literal["move", "list_move", "status"]
    data: str  # ha senso solamente per la move, e definisce la mossa e.g. e2e4

class GameResponse(BaseModel):
    kind: Literal["status"] # add with other types
    data: GameStatusResponse
