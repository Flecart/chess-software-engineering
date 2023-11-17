from pydantic import BaseModel

class CreateGameRequest(BaseModel):
    against_bot: bool = True
    type: str = 'dark_chess' # default value
    # Other fields that might be useful next
    # color: str = 'white'
    #time: (int,int) = (3,3) 
    #increment: (int,int) = (0,0) 

    
class GameStatusResponse(BaseModel):
    fen: str
    finished: bool
    possible_moves: list[str] | None = None
    view:str
    move_made: str | None
    # time_white: datetime.deltatime|None  #should also be added from when
    # time_balck: datetime.deltatime|None

