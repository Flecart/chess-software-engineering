from pydantic import BaseModel
import datetime
from typing import Literal

class CreateGameRequest(BaseModel):
    against_bot: bool = True
    type: str = 'dark_chess' # default value
    # Other fields that might be useful next
    # color: str = 'white'
    #time: (int,int) = (3,3) 
    #increment: (int,int) = (0,0) 

    
class GameStatusResponse(BaseModel):
    ended: bool
    possible_moves: list[str] | None = None
    view: str
    move_made: str | None
    turn: Literal["white", "black"]
    time_left_white:str|None  #should also be added from when
    time_left_black: str|None
    time_start_white: str|None
    time_start_black: str|None

    

